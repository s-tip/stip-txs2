import core.const as const


def _is_exist_http_accept(headers):
    return const.HTTP_ACCEPT_KEY in headers


def _is_exist_http_content_type(headers):
    return const.HTTP_CONTENT_TYPE in headers


def _is_exist_http_content_length(headers):
    return const.HTTP_CONTENT_TYPE in headers


def _parse_http_header_value(val):
    if ';' not in val:
        return val, None
    items = val.split(';')
    content_value = items[0].strip()
    d = {}
    for item in items[1:]:
        kv = item.split('=')
        try:
            d[kv[0].strip()] = kv[1].strip()
        except IndexError:
            pass
    return content_value, d


def get_version_from_accept(headers):
    if not _is_exist_http_accept(headers):
        return -1
    accept = headers[const.HTTP_ACCEPT_KEY]
    content_value, dict_ = _parse_http_header_value(accept)
    if content_value != const.ACCEPT_TAXII_JSON:
        return -1
    if not dict_:
        return const.TAXII_VERSION
    if 'version' not in dict_:
        return const.TAXII_VERSION
    try:
        return float(dict_['version'])
    except ValueError:
        print('Invalid Accept: %s' % (accept))
        return -1


def get_version_from_content_type(headers):
    if not _is_exist_http_content_type(headers):
        return -1
    content_type = headers[const.HTTP_CONTENT_TYPE]
    content_value, dict_ = _parse_http_header_value(content_type)
    if not dict_:
        return -1
    if content_value != const.ACCEPT_TAXII_JSON:
        return -1
    if 'version' not in dict_:
        return const.TAXII_VERSION
    try:
        return float(dict_['version'])
    except ValueError:
        print('Invalid ContentType: %s' % (content_type))
        return -1


def get_content_length(headers):
    try:
        return int(headers[const.HTTP_CONTENT_LENGTH])
    except KeyError:
        return -1
    except ValueError:
        return -1
