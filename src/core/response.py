import json
import pytz
import datetime
import traceback
import django.http.response as django_resp
import core.const as const
from core.logger import debug_response
from django.views.decorators.csrf import csrf_exempt


def get_taxii_date_str(dt):
    return dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def get_response_header(objects):
    if len(objects) == 0:
        return None
    first = None
    last = None
    for object_ in objects:
        if not first:
            first = object_.added
        else:
            if object_.added < first:
                first = object_.added
        if not last:
            last = object_.added
        else:
            if object_.added > last:
                last = object_.added
    response_header = {}
    response_header['X-TAXII-Date-Added-First'] = get_taxii_date_str(first)
    response_header['X-TAXII-Date-Added-Last'] = get_taxii_date_str(last)
    return response_header


def ok(payload=None, response_header=None):
    content = None
    if payload is not None:
        if isinstance(payload, dict):
            content = json.dumps(payload)
    content_type = const.HTTP_RESPONSE_CONTENT_TYPE
    status = 200
    response = django_resp.HttpResponse(
        content=content,
        content_type=content_type,
        status=status)
    if response_header:
        for key in response_header.keys():
            response[key] = response_header[key]
    debug_response(content, None, content_type, status)
    return response


def accepted(payload):
    content = json.dumps(payload)
    status = 202
    content_type = const.HTTP_RESPONSE_CONTENT_TYPE
    response = django_resp.HttpResponse(
        content=content,
        status=status,
        content_type=content_type)
    debug_response(content, None, content_type, status)
    return response


def unauhorized():
    payload = _get_error_payload(
        'Unauthorized',
        'Unauthorized',
        '401')
    content_type = const.HTTP_RESPONSE_CONTENT_TYPE
    response = django_resp.HttpResponse(
        content=json.dumps(payload),
        status=401,
        content_type=content_type)
    response['WWW-Authenticate'] = 'Basic realm="basic auth username/password invalid"'
    debug_response(None, None, content_type, 401)
    return response


def invalid_accept():
    HTTP_RESPONSE_INVALID_ACCEPT = 406
    payload = _get_error_payload(
        'Not Acceptable',
        'Not Acceptable',
        str(HTTP_RESPONSE_INVALID_ACCEPT))
    content = json.dumps(payload)
    content_type = const.HTTP_RESPONSE_CONTENT_TYPE
    status = HTTP_RESPONSE_INVALID_ACCEPT
    response = django_resp.HttpResponse(
        content=content,
        status=status,
        content_type=content_type)
    debug_response(content, None, content_type, status)
    return response


def not_allowed(methods):
    payload = _get_error_payload(
        'Method Not Allowed',
        'Method Not Allowed',
        '405')
    content = json.dumps(payload)
    content_type = const.HTTP_RESPONSE_CONTENT_TYPE
    response = django_resp.HttpResponseNotAllowed(
        methods,
        content=json.dumps(payload),
        content_type=const.HTTP_RESPONSE_CONTENT_TYPE)
    debug_response(content, None, content_type, 405)
    return response


@csrf_exempt
def not_found(*args, **kwargs):
    payload = _get_error_payload(
        'Not Found',
        'Not Found',
        '404')
    content = json.dumps(payload)
    content_type = const.HTTP_RESPONSE_CONTENT_TYPE
    response = django_resp.HttpResponseNotFound(
        content=content,
        content_type=content_type)
    debug_response(content, None, content_type, 404)
    return response


def forbidden():
    payload = _get_error_payload(
        'Forbidden',
        'Forbiden',
        '403')
    content = json.dumps(payload)
    content_type = const.HTTP_RESPONSE_CONTENT_TYPE
    response = django_resp.HttpResponseForbidden(
        content=content,
        content_type=content_type)
    debug_response(content, None, content_type, 403)
    return response


def bad_request(reason='Bad Request'):
    payload = _get_error_payload(
        'Bad Request',
        reason,
        '400')
    content = json.dumps(payload)
    content_type = const.HTTP_RESPONSE_CONTENT_TYPE
    response = django_resp.HttpResponseBadRequest(
        content=content,
        content_type=content_type)
    debug_response(content, None, content_type, 400)
    return response


def payload_too_large():
    HTTP_RESPONSE_PAYLOAD_TOO_LARGE = 413
    payload = _get_error_payload(
        'Payload Too Long',
        'Payload Too Long',
        str(HTTP_RESPONSE_PAYLOAD_TOO_LARGE))
    content = json.dumps(payload)
    status = HTTP_RESPONSE_PAYLOAD_TOO_LARGE
    content_type = const.HTTP_RESPONSE_CONTENT_TYPE
    response = django_resp.HttpResponse(
        content=content,
        status=status,
        content_type=content_type)
    debug_response(content, None, content_type, status)
    return response


def unsupported_media_type():
    HTTP_RESPONSE_UNSUPPORTED_MEDIA_TYPE = 415
    payload = _get_error_payload(
        'Unsupported Media Type',
        'Unsupported Media Type',
        str(HTTP_RESPONSE_UNSUPPORTED_MEDIA_TYPE))
    content = json.dumps(payload)
    status = HTTP_RESPONSE_UNSUPPORTED_MEDIA_TYPE
    content_type = const.HTTP_RESPONSE_CONTENT_TYPE
    response = django_resp.HttpResponse(
        content=content,
        status=status,
        content_type=content_type)
    debug_response(content, None, content_type, status)
    return response


def server_error(e):
    try:
        traceback.print_exc()
        payload = _get_error_payload(
            'Internal Server Error',
            str(e),
            '500'
        )
        details = {}
        details['message'] = str(e)
        details['args'] = str(e.args)
        payload['details'] = details
        content = json.dumps(payload)
    except Exception:
        traceback.print_exc()
        content = {}
    content_type = const.HTTP_RESPONSE_CONTENT_TYPE
    response = django_resp.HttpResponseServerError(
        content=content,
        content_type=content_type)
    debug_response(content, None, content_type, 500)
    return response


def _get_error_payload(title, description, http_status):
    payload = {}
    dt_str = get_taxii_date_str(datetime.datetime.now(pytz.utc))
    payload['title'] = 'S-TIP TAXII2 Server: %s' % (title)
    payload['description'] = '%s (%s/GMT)' % (description, dt_str)
    payload['http_status'] = http_status
    payload['error_id'] = ''
    payload['error_code'] = ''
    payload['external_details'] = ''
    payload['details'] = {}
    return payload
