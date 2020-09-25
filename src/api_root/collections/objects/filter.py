from ctirs.core.mongo.documents_taxii21_objects import StixManifest, StixObject
import core.const as const


def _query_parameters_without_version(query, communities):
    parameters = {}
    if communities:
        filter_communities = []
        for community in communities:
            filter_communities.append(community.id)
        parameters['community'] = {'$in': filter_communities}
    else:
        parameters['community'] = {'$in': []}
    if 'added_after' in query:
        parameters['added'] = {'$gt': query['added_after']}

    if 'match' not in query:
        return parameters

    match = query['match']
    if 'type' in match:
        types_ = match['type']
        parameters['object_type'] = {'$in': types_}

    if 'id' in match:
        ids_ = match['id']
        parameters['object_id'] = {'$in': ids_}

    if 'spec_version' in match:
        spec_versions = match['spec_version']
        parameters['spec_version'] = {'$in': spec_versions}
    parameters['deleted'] = {'$eq': False}
    return parameters


def _get_version_filter(query, pipeline):
    version_selector = []
    if 'match' not in query:
        versions = ['last']
    else:
        if 'version' not in query['match']:
            versions = ['last']
        else:
            versions = query['match']['version']

    if 'all' in versions:
        return pipeline

    if 'first' in versions:
        version_selector.append({'$arrayElemAt': ['$versions', 0]})
        versions.remove('first')
    if 'last' in versions:
        version_selector.append({'$arrayElemAt': ['$versions', -1]})
        versions.remove('last')
    is_exist_actual_version = False
    for version in versions:
        is_exist_actual_version = True
        version_selector.append(
            {
                '$arrayElemAt': [
                    '$versions', {
                        '$indexOfArray': ['$versions', version]
                    }
                ]
            }
        )

    if is_exist_actual_version:
        initial_match_fliter = pipeline[0]
        match_cond = initial_match_fliter['$match']
        match_cond['$and'].append({'versions': {'$all': versions}})

    version_filter = {
        '$addFields': {
            'versions': version_selector
        }
    }
    pipeline.append(version_filter)
    return pipeline


def _add_pagination(pipeline, query):
    pipeline.append({'$sort': {'added': 1}})

    if 'next' in query:
        try:
            pipeline.append({'$skip': int(query['next'])})
        except ValueError:
            pass

    cursor = StixManifest.objects.aggregate(*pipeline)
    remaining = len(list(cursor))

    if 'limit' in query:
        try:
            limit = query['limit']
        except ValueError:
            limit = const.DEFAULT_LIMIT
        pipeline.append({'$limit': limit})
    return remaining, pipeline


def apply_filter(query, communities):
    base_query = _query_parameters_without_version(query, communities)
    match_filter = {
        '$match': {
            '$and': [base_query],
        },
    }
    pipeline = [match_filter]

    pipeline = _get_version_filter(query, pipeline)

    join_objects = {
        '$lookup': {
            'from': 'stix_object',
            'localField': '_id',
            'foreignField': 'manifest',
            'as': 'obj',
        }
    }
    pipeline.append(join_objects)

    add_versions = {
        '$addFields': {'obj.versions': '$versions'},
    }
    pipeline.append(add_versions)
    pipeline.append({'$unwind': '$obj'})
    pipeline.append({'$replaceRoot': {'newRoot': '$obj'}})

    # redaction
    redact_objects_by_versions = {
        '$redact': {
            '$cond': {
                'if': {
                    '$switch': {
                        'branches': [{
                            'case': {'$in': ['$modified', '$versions']},
                            'then': True
                        }],
                        'default': False,
                    }
                },
                'then': '$$KEEP',
                'else': '$$PRUNE',
            }
        }
    }
    pipeline.append(redact_objects_by_versions)

    redact_objects_by_stix_objects = {
        '$redact': {
            '$cond': {
                'if': {
                    '$eq': ['$deleted', True]
                },
                'then': '$$PRUNE',
                'else': '$$KEEP',
            }
        }
    }
    pipeline.append(redact_objects_by_stix_objects)

    pipeline.append({'$project': {'versions': 0}})

    cursor = StixManifest.objects.aggregate(*pipeline)

    remaining, pipeline = _add_pagination(pipeline, query)

    cursor = StixManifest.objects.aggregate(*pipeline)
    ret = []
    for doc in cursor:
        stix_object = StixObject.objects.get(id=doc['_id'])
        ret.append(stix_object)
    return remaining, ret
