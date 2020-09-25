import json
import threading
import core.response as taxii_resp
import core.request_header as rh
import core.const as const
from django.views.decorators.csrf import csrf_exempt
from auth.basic_auth import get_basic_auth
from core.request_query import parse_query
from api_root.models import ApiRoot
from api_root.status.models import Status
from .filter import apply_filter
from .post import async_post
from ctirs.core.mongo.documents_taxii21_objects import StixManifest, StixObject
from ctirs.core.mongo.documents import Communities
from decolators import get_required, get_post_required, get_delete_required


@csrf_exempt
@get_post_required
def objects(request, api_root_name, collection_id):
    try:
        if not ApiRoot.auth_check(request, api_root_name):
            return taxii_resp.unauhorized()
        collection = ApiRoot.get_collection(api_root_name, collection_id)
        if not collection:
            return taxii_resp.not_found()
        query = parse_query(request)
        if request.method == 'GET':
            if collection['can_read']:
                return _objects_get(api_root_name, collection, query)
            else:
                return taxii_resp.forbidden()
        else:
            if collection['can_write']:
                return _objects_post(request, api_root_name, collection)
            else:
                return taxii_resp.forbidden()
    except ApiRoot.DoesNotExist:
        return taxii_resp.not_found()
    except Exception as e:
        return taxii_resp.server_error(e)


@csrf_exempt
@get_delete_required
def object_(request, api_root_name, collection_id, object_id):
    try:
        if not ApiRoot.auth_check(request, api_root_name):
            return taxii_resp.unauhorized()
        collection = ApiRoot.get_collection(api_root_name, collection_id)
        if not collection:
            return taxii_resp.not_found()
        query = parse_query(request)
        if request.method == 'GET':
            if collection['can_read']:
                return _object_get(api_root_name, collection, object_id, query)
            else:
                return taxii_resp.forbidden()
        elif request.method == 'DELETE':
            if not collection['can_read'] and not collection['can_write']:
                return taxii_resp.not_found()
            if collection['can_read'] and not collection['can_write']:
                return taxii_resp.forbidden()
            if not collection['can_read'] and collection['can_write']:
                return taxii_resp.forbidden()
            return _object_delete(api_root_name, collection, object_id, query)
    except ApiRoot.DoesNotExist:
        return taxii_resp.not_found()
    except Exception as e:
        return taxii_resp.server_error(e)


@csrf_exempt
@get_required
def manifest(request, api_root_name, collection_id):
    try:
        if not ApiRoot.auth_check(request, api_root_name):
            return taxii_resp.unauhorized()
        collection = ApiRoot.get_collection(api_root_name, collection_id)
        if not collection:
            return taxii_resp.not_found()
        query = parse_query(request)
        if collection['can_read']:
            return _manifest_get(api_root_name, collection, query)
        else:
            return taxii_resp.forbidden()
    except ApiRoot.DoesNotExist:
        return taxii_resp.not_found()
    except Exception as e:
        return taxii_resp.server_error(e)


@csrf_exempt
@get_required
def versions(request, api_root_name, collection_id, object_id):
    try:
        if not ApiRoot.auth_check(request, api_root_name):
            return taxii_resp.unauhorized()
        collection = ApiRoot.get_collection(api_root_name, collection_id)
        if not collection:
            return taxii_resp.not_found()
        if not collection['can_read']:
            return taxii_resp.forbidden()

        can_read_communities = _get_can_read_communities(collection)
        if StixObject.objects.filter(object_id=object_id, community__in=can_read_communities).count() == 0:
            return taxii_resp.not_found()

        more = False
        query = parse_query(request)
        objects = []
        versions_list = []

        query = _set_object_id_in_query(query, object_id)
        limit, next_ = _pagination_info(query)
        index = 0
        remaining, cursor = apply_filter(query, can_read_communities)
        for doc in cursor:
            if doc.deleted:
                continue
            stix_objects = StixObject.objects.filter(
                object_id=doc.object_id,
                community__in=can_read_communities)
            for stix_object in stix_objects:
                if not stix_object.deleted:
                    objects.append(stix_object)
                    versions_list.append(stix_object.modified)
            index += 1
            remaining -= 1
            if index == limit:
                if remaining > 0:
                    more = True
                break

        versions = {}
        versions['more'] = more
        versions['versions'] = versions_list
        response_header = taxii_resp.get_response_header(objects)
        return taxii_resp.ok(versions, response_header=response_header)
    except ApiRoot.DoesNotExist:
        return taxii_resp.not_found()
    except Exception as e:
        return taxii_resp.server_error(e)


def _pagination_info(query):
    limit = query['limit']
    next_ = int(query['next']) if 'next' in query else 0
    return limit, next_


def _objects_get(api_root_name, collection, query):
    try:
        envelop = {}
        envelop['more'] = False
        envelop['objects'] = []
        objects = []

        limit, next_ = _pagination_info(query)
        index = 0
        remaining, cursor = apply_filter(
            query,
            _get_can_read_communities(collection))
        for stix_object in cursor:
            if stix_object.deleted:
                continue
            envelop['objects'].append(stix_object.object_value)
            objects.append(stix_object)
            index += 1
            remaining -= 1
            if index == limit:
                if remaining > 0:
                    envelop['more'] = True
                    envelop['next'] = str(next_ + limit)
                break
        response_header = taxii_resp.get_response_header(objects)
        return taxii_resp.ok(envelop, response_header=response_header)
    except Exception as e:
        return taxii_resp.server_error(e)


def _objects_post(request, api_root_name, collection):
    try:
        if rh.get_version_from_content_type(request.META) < const.TAXII_VERSION:
            return taxii_resp.unsupported_media_type()
        stip_user = get_basic_auth(request.META)
        if not stip_user:
            return taxii_resp.unauhorized()
        content_length = rh.get_content_length(request.META)
        max_content_length = ApiRoot.get_max_content_length(api_root_name)
        if content_length > max_content_length:
            return taxii_resp.payload_too_large()
        try:
            community = collection.stip_meta['can_write_community']
        except Exception:
            return taxii_resp.server_error(Exception('No community for publish'))

        envelop = json.loads(request.body)
        taxii2_status = Status.create(envelop['objects'])

        args = [envelop, collection, taxii2_status, stip_user, community]
        th = threading.Thread(target=async_post, args=args)
        th.start()

        payload = taxii2_status.get_status()
        return taxii_resp.accepted(payload)
    except Exception as e:
        return taxii_resp.server_error(e)


def _get_manifest_record(stix_object, media_type):
    manifest_record = {}
    manifest_record['id'] = stix_object.object_id
    manifest_record['date_added'] = taxii_resp.get_taxii_date_str(
        stix_object.added)
    manifest_record['version'] = stix_object.modified
    manifest_record['media_type'] = media_type
    return manifest_record


def _manifest_get(api_root_name, collection, query):
    try:
        manifest_records = []
        objects = []

        limit, next_ = _pagination_info(query)
        index = 0
        more = False
        remaining, manifests = apply_filter(
            query,
            _get_can_read_communities(collection))
        for stix_object in manifests:
            if stix_object.deleted:
                continue
            stix_manifest = StixManifest.objects.get(
                object_id=stix_object.object_id)

            manifest_record = _get_manifest_record(
                stix_object,
                stix_manifest.media_types[0])
            manifest_records.append(manifest_record)
            objects.append(stix_object)
            index += 1
            remaining -= 1
            if index == limit:
                if remaining > 0:
                    more = True
        if len(manifest_records) == 0:
            return taxii_resp.ok({})
        manifest = {}
        manifest['more'] = more
        manifest['objects'] = manifest_records
        response_header = taxii_resp.get_response_header(objects)
        return taxii_resp.ok(manifest, response_header=response_header)
    except Exception as e:
        return taxii_resp.server_error(e)


def _get_can_read_communities(collection):
    try:
        return collection.stip_meta['can_read_communities']
    except Exception:
        return None


def _get_can_write_communities(collection):
    try:
        return [collection.stip_meta['can_write_community']]
    except Exception:
        return None


def _object_get(api_root_name, collection, object_id, query):
    try:
        envelop = {}
        envelop['more'] = False
        envelop['objects'] = []
        objects = []

        can_read_communities = _get_can_read_communities(collection)
        if StixObject.objects.filter(object_id=object_id, community__in=can_read_communities).count() == 0:
            return taxii_resp.not_found()

        query = _set_object_id_in_query(query, object_id)
        limit, next_ = _pagination_info(query)
        index = 0
        remaining, cursor = apply_filter(query, can_read_communities)
        for stix_object in cursor:
            if stix_object.deleted:
                continue
            objects.append(stix_object)
            envelop['objects'].append(stix_object.object_value)
            index += 1
            remaining -= 1
            if index == limit:
                if remaining > 0:
                    envelop['more'] = True
                    envelop['next'] = str(next_ + limit)
                break
        response_header = taxii_resp.get_response_header(objects)
        return taxii_resp.ok(envelop, response_header=response_header)
    except Exception as e:
        return taxii_resp.server_error(e)


def _object_delete(api_root_name, collection, object_id, query):
    try:
        query = _set_object_id_in_query(query, object_id)
        _, cursor = apply_filter(
            query,
            _get_can_write_communities(collection))
        for stix_object in cursor:
            modified = stix_object.modified
            stix_object.deleted = True
            stix_object.save()
            stix_manifest = StixManifest.objects.get(
                object_id=stix_object.object_id)
            stix_manifest.deleted_versions.append(modified)
            stix_manifest.versions.remove(modified)
            if len(stix_manifest.versions) == 0:
                stix_manifest.deleted = True
            stix_manifest.save()
        return taxii_resp.ok({})
    except Exception as e:
        return taxii_resp.server_error(e)


def _set_object_id_in_query(query, object_id, ignore_version=False):
    if 'match' not in query:
        match = {}
        match['id'] = [object_id]
        query['match'] = match
    else:
        query['match']['id'] = [object_id]
        if 'type' in query['match']:
            del query['match']['type']
        if ignore_version:
            if 'version' in query['match']:
                del query['match']['version']
    return query
