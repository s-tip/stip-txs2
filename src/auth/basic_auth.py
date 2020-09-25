import base64
import traceback
import django.contrib.auth
import core.const as const


def _is_exist_http_authorization(headers):
    return const.HTTP_AUTH_KEY in headers


def get_basic_auth(headers):
    try:
        if not _is_exist_http_authorization(headers):
            return None
        (auth_scheme, base64_username_pass) = headers[const.HTTP_AUTH_KEY].split(' ', 1)
        if auth_scheme.lower() != 'basic':
            return None
        username_pass = base64.decodebytes(
            base64_username_pass.strip().encode('ascii')).decode('ascii')
        (username, password) = username_pass.split(':', 1)
        stip_user = django.contrib.auth.authenticate(
            username=username,
            password=password)
        return stip_user if stip_user else None
    except Exception:
        traceback.print_exc()
        return None
