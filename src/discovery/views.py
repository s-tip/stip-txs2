import core.response as taxii_resp
from django.views.decorators.csrf import csrf_exempt
from discovery.models import Discovery
from decolators import get_required, auth_check


@csrf_exempt
@get_required
def discovery(request):
    try:
        if not auth_check(request):
            return taxii_resp.unauhorized()
        payload = Discovery.get_discovery_response()
        return taxii_resp.ok(payload)
    except Exception as e:
        return taxii_resp.server_error(e)
