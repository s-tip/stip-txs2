import core.response as taxii_resp
from django.views.decorators.csrf import csrf_exempt
from core.logger import debug_request, get_logger
from .models import ApiRoot
from decolators import get_required

logger = get_logger()


@csrf_exempt
@get_required
def api_root(request, api_root_name):
    try:
        debug_request(request)
        logger.info('request:api_root_name: %s' % (api_root_name))
        user = ApiRoot.auth_check(request, api_root_name)
        logger.info('request:user: %s' % (user))
        if not user:
            return taxii_resp.unauhorized()
        api_root = ApiRoot.get_api_root(api_root_name)
        if api_root:
            return taxii_resp.ok(api_root)
        return taxii_resp.not_found()
    except ApiRoot.DoesNotExist:
        return taxii_resp.not_found()
    except Exception as e:
        return taxii_resp.server_error(e)
