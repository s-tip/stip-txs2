import core.response as taxii_resp
from django.views.decorators.csrf import csrf_exempt
from api_root.models import ApiRoot
from decolators import get_required


@csrf_exempt
@get_required
def collections(request, api_root_name):
    try:
        if not ApiRoot.auth_check(request, api_root_name):
            return taxii_resp.unauhorized()
        collections = ApiRoot.get_collections(api_root_name)
        if not collections:
            return taxii_resp.not_found()
        resp = {'collections': collections}
        return taxii_resp.ok(resp)
    except ApiRoot.DoesNotExist:
        return taxii_resp.not_found()
    except Exception as e:
        return taxii_resp.server_error(e)


@csrf_exempt
@get_required
def collection(request, api_root_name, collection_id):
    try:
        if not ApiRoot.auth_check(request, api_root_name):
            return taxii_resp.unauhorized()
        collection = ApiRoot.get_collection(api_root_name, collection_id)
        if collection:
            return taxii_resp.ok(collection.get_collection_info())
        return taxii_resp.not_found()
    except ApiRoot.DoesNotExist:
        return taxii_resp.not_found()
    except Exception as e:
        return taxii_resp.server_error(e)
