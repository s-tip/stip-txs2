import datetime
import pytz
import core.const as const


def parse_query(request):
    _check_duplicate_params(request)
    queries = {}
    # added_after
    if request.GET.get('added_after'):
        dt = str2datetime(request.GET.get('added_after'))
        if dt:
            queries['added_after'] = dt
    # limit
    queries['limit'] = const.DEFAULT_LIMIT
    if request.GET.get('limit'):
        try:
            limit = int(request.GET.get('limit'))
            if limit > 0:
                queries['limit'] = int(limit)
        except ValueError:
            pass
    # next
    if request.GET.get('next'):
        queries['next'] = request.GET.get('next')

    # match
    queries['match'] = _parse_query_match(request)
    return queries


def str2datetime(s):
    try:
        dt = datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%fZ')
        return dt.replace(tzinfo=pytz.utc)
    except ValueError:
        return None


def _check_duplicate_params(request):
    query_params = {}
    for param in request.META["QUERY_STRING"].split('&'):
        kv = param.split('=')
        if len(kv) < 2:
            continue
        if kv[0] in query_params:
            raise Exception('Duplicate parameter (%s)' % (kv[0]))
        query_params[kv[0]] = kv[1]
    return query_params


def _parse_query_value_list(s):
    rtn = []
    for item in s.split(','):
        rtn.append(item)
    return list(set(rtn))


def _parse_query_match(request):
    match = {}
    keys = [
        'id', 'spec_version', 'type', 'version',
        # -----
        #'source_ref', 'target_ref', 'relationship_type',
        #'sighting_of_ref', 'object_marking_refs',
        #'tlp', 'external_id', 'source_name', 'created_by_ref',
        #'confidence', 'sectors', 'labels', 'object_refs', 'value',
    ]

    for key in keys:
        query_key = 'match[%s]' % (key)
        if request.GET.get(query_key):
            match[key] = _parse_query_value_list(request.GET.get(query_key))
    return match
