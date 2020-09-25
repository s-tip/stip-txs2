import uuid
import json
import mongoengine as me
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api_root.collections.models import Collection
from api_root.models import ApiRoot
from ctirs.core.mongo.documents import Communities
from core.const import DEFAULT_MEDIA_TYPES
from console.error.views import error
from console.decorators import admin_required


@admin_required
def collections(request):
    try:
        collections = Collection.objects
        communities = Communities.objects
        return render(
            request,
            'collections.html',
            {
                'collections': collections,
                'communities': communities
            })
    except Exception as e:
        return error(request, str(e))


@admin_required
def create_modify(request):
    try:
        data = json.loads(request.POST['data'])
        col_id = data['id']
        title = data['title']
        description = data['description']
        alias = data['alias']
        can_read = data['can_read']
        can_write = data['can_write']
        action = data['action']
        can_read_communities = None
        can_write_community = None

        if can_read:
            can_read_communities = []
            for name in data['can_read_communities']:
                can_read_communities.append(Communities.objects.get(name=name))

        if can_write:
            can_write_community = Communities.objects.get(name=data['can_write_community'])

        if action == 'create':
            media_types = DEFAULT_MEDIA_TYPES
        else:
            media_types = None

        Collection.update_or_create(
            col_id,
            title,
            description,
            alias,
            can_read,
            can_write,
            media_types,
            can_read_communities=can_read_communities,
            can_write_community=can_write_community,
        )
        return redirect('collections')
    except Exception as e:
        return error(request, str(e))


@admin_required
def delete(request):
    try:
        data = json.loads(request.POST['data'])
        col_id = data['col_id']
        col = Collection.objects.get(col_id=col_id)
        for api_root in ApiRoot.objects:
            if col in api_root.collections:
                api_root.collections.remove(col)
                api_root.save()
        col.delete()
        return redirect('collections')
    except me.DoesNotExist:
        print(col_id + ' does not exist.')
        return redirect('collections')
    except Exception as e:
        return error(request, str(e))


@admin_required
def generate_uuid(request):
    try:
        return JsonResponse({'uuid': str(uuid.uuid4())})
    except Exception as e:
        return error(request, str(e))


@csrf_exempt
@admin_required
def get_access_authority(request):
    try:
        col_id = request.POST['col_id']
        col = Collection.objects.get(col_id=col_id)
        d = {}
        if 'can_read_communities' in col.stip_meta:
            d['can_read_communities'] = []
            for community in col.stip_meta['can_read_communities']:
                d['can_read_communities'].append(community.name)
        else:
            d['can_read_communities'] = None
        if 'can_write_community' in col.stip_meta:
            d['can_write_community'] = col.stip_meta['can_write_community'].name
        else:
            d['can_write_community'] = None
        return JsonResponse(d)
    except Exception as e:
        return error(request, str(e))
