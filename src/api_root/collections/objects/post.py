import tempfile
import os
from stix2.v21 import Bundle
from ctirs.core.mongo.documents_taxii21_objects import StixObject, get_modified_from_object
import ctirs.models.sns.feeds.rs as rs


def async_post(envelop, collection, taxii2_status, stip_user, community):
    pendings = []
    bundle_objects = []
    for object_ in envelop['objects']:
        try:
            object_id = object_['id']
            if 'modified' not in object_:
                msg = 'No modified(id: %s)' % (object_id)
                taxii2_status.failure(object_id, object_['created'], msg)
                continue
            modified = get_modified_from_object(object_)
            objects = StixObject.objects.filter(
                object_id=object_id,
                modified=modified)
            is_exist = False
            for object__ in objects:
                if not object__.deleted:
                    is_exist = True
                    break
            if is_exist:
                msg = 'Duplication Object(id: %s, modifed: %s)' % (object_id, modified)
                taxii2_status.failure(object_id, modified, msg)
                continue
        except StixObject.DoesNotExist:
            pass
        bundle_objects.append(object_)
        pendings.append((object_id, modified))

    if len(bundle_objects) == 0:
        return

    bundle = Bundle(bundle_objects, allow_custom=True)

    try:
        _, stix2_file_path = tempfile.mkstemp()
        with open(stix2_file_path, 'w', encoding='utf-8') as fp:
            fp.write(bundle.serialize(
                True,
                ensure_ascii=False,
                include_optional_defaults=True))
        rs.regist_ctim_rs(stip_user, bundle.id, stix2_file_path, community.name)
    except Exception as e:
        raise(e)
    finally:
        try:
            os.remove(stix2_file_path)
        except Exception:
            pass

    for object_id, modified in pendings:
        taxii2_status.success(object_id, modified)

    return
