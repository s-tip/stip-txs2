import core.response as taxii_resp
from django.views.decorators.csrf import csrf_exempt
from decolators import get_required
from .models import Status
from api_root.models import ApiRoot


@csrf_exempt
@get_required
def status(request, api_root_name, status_id):
    try:
        if not ApiRoot.auth_check(request, api_root_name):
            return taxii_resp.unauhorized()
        status = Status.objects.get(status_id=status_id)
    except Status.DoesNotExist:
        return taxii_resp.not_found()
    return taxii_resp.ok(status.get_status())
