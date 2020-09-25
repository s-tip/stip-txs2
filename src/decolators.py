import core.response as taxii_resp
from core.const import TAXII_VERSION
from auth.basic_auth import get_basic_auth
from core.request_header import get_version_from_accept


def get_post_required(f):
    def wrap(request, *args, **kwargs):
        if request.method != 'GET' and request.method != 'POST':
            return taxii_resp.not_allowed(['GET', 'POST'])
        if not _accept_check(request):
            return taxii_resp.invalid_accept()
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def get_delete_required(f):
    def wrap(request, *args, **kwargs):
        if request.method != 'GET' and request.method != 'DELETE':
            return taxii_resp.not_allowed(['GET', 'DELETE'])
        if not _accept_check(request):
            return taxii_resp.invalid_accept()
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def get_required(f):
    def wrap(request, *args, **kwargs):
        if request.method != 'GET':
            return taxii_resp.not_allowed(['GET'])
        if not _accept_check(request):
            return taxii_resp.invalid_accept()
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def auth_check(request, allowed_users=None):
    stip_user = get_basic_auth(request.META)
    if not stip_user:
        return None
    if allowed_users:
        if stip_user.username not in allowed_users:
            return None
    return stip_user


def _accept_check(request):
    return get_version_from_accept(request.META) >= TAXII_VERSION
