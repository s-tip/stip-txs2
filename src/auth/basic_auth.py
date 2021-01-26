import base64
import traceback
import core.const as const
from stip.common.rest_api_auth import auth_by_api_key


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
        (username, api_key) = username_pass.split(':', 1)
        return auth_by_api_key(username, api_key)
    except Exception:
        traceback.print_exc()
        return None
