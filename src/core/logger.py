from logging import getLogger
from urllib.parse import unquote

logger = getLogger('txs2_audit')


def get_logger():
    return logger


def debug_request(request):
    logger.info('-----start-----')
    logger.info('request:method: %s' % (request.method))
    logger.info('request:path: %s' % (request.path))
    logger.info('request:header(HTTP_ACCEPT): %s' % (request.META.get('HTTP_ACCEPT')))
    logger.info('request:header(HTTP_AUTHORIZATION): %s' % (request.META.get('HTTP_AUTHORIZATION')))
    logger.info('request:header(HTTP_USER_AGENT): %s' % (request.META.get('HTTP_USER_AGENT')))
    logger.info('request:header(CONTENT_TYPE): %s' % (request.META.get('CONTENT_TYPE')))
    query_str = request.META.get('QUERY_STRING')
    logger.info('request:header(QUERY_STRING): %s' % (query_str))
    queries = query_str.split('&')
    if len(queries) != 0:
        for query in queries:
            q = query.split('=')
            if len(q) == 2:
                logger.info('request:header(QUERY_STRING/item): %s=%s' % (unquote(q[0]), unquote(q[1])))
    logger.info('request:header(REMOTE_ADDR): %s' % (request.META.get('REMOTE_ADDR')))
    return


def debug_response(content, header, content_type, status):
    logger.info('response:content: %s' % (content))
    logger.info('response:header: %s' % (None))
    logger.info('response:content_type: %s' % (content_type))
    logger.info('response:status: %d' % (status))
    logger.info('-----end-----')
    return