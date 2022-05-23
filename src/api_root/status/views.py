import core.response as taxii_resp
from django.views.decorators.csrf import csrf_exempt
from decolators import get_required
from .models import Status
from core.logger import debug_request, get_logger
from api_root.models import ApiRoot

logger = get_logger()


@csrf_exempt
@get_required
def status(request, api_root_name, status_id):
    try:
        debug_request(request)
        logger.info('request:api_root_name: %s' % (api_root_name))
        logger.info('request:status_id: %s' % (status_id))
        user = ApiRoot.auth_check(request, api_root_name)
        logger.info('request:user: %s' % (user))
        if not user:
            return taxii_resp.unauhorized()
        status = Status.objects.get(status_id=status_id)
    except ApiRoot.DoesNotExist:
        return taxii_resp.not_found()
    except Status.DoesNotExist:
        return taxii_resp.not_found()
    return taxii_resp.ok(status.get_status())
