import core.response as taxii_resp
from django.views.decorators.csrf import csrf_exempt
from core.logger import debug_request, get_logger
from discovery.models import Discovery
from decolators import get_required, auth_check

logger = get_logger()


@csrf_exempt
@get_required
def discovery(request):
    try:
        debug_request(request)
        user = auth_check(request)
        logger.info('request:user: %s' % (user))
        if not user:
            return taxii_resp.unauhorized()
        payload = Discovery.get_discovery_response()
        return taxii_resp.ok(payload)
    except Exception as e:
        return taxii_resp.server_error(e)
