import json
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from discovery.models import Discovery
from api_root.models import ApiRoot
from api_root.collections.models import Collection
from core.const import DEFAULT_VERSIONS
from console.error.views import error
from console.decorators import admin_required
from ctirs.models import STIPUser


@admin_required
def api_roots(request):
    try:
        api_roots = ApiRoot.objects
        collections = Collection.objects
        users = STIPUser.objects.filter(is_active=True)
        return render(
            request,
            'api_roots.html',
            {
                'api_roots': api_roots,
                'collections': collections,
                'users': users,
            })
    except Exception as e:
        return error(request, str(e))


@admin_required
def create_modify(request):
    RESERVED_API_ROOT_NAMES = ['taxii', 'taxii2']
    try:
        data = json.loads(request.POST['data'])
        api_root_name = data['api_root_name']
        title = data['title']
        description = data['description']
        max_content_length = int(data['max_content_length'])
        action = data['action']
        collections = data['collections']
        users = data['users']
        if action == 'create':
            versions = DEFAULT_VERSIONS
        else:
            versions = None
        if api_root_name in RESERVED_API_ROOT_NAMES:
            raise Exception('%s is reserved.' % (api_root_name))
        api_root = ApiRoot.update_or_create(api_root_name, title, description, versions, max_content_length)
        api_root.set_collections(collections)
        api_root.set_users(users)
        if action == 'create':
            Discovery.append_api_root(api_root)
        return redirect('api_roots')
    except Exception as e:
        return error(request, str(e))


@admin_required
def delete(request):
    try:
        data = json.loads(request.POST['data'])
        api_root_name = data['api_root_name']
        api_root = ApiRoot.objects.get(name=api_root_name)
        discovery = Discovery.objects.get()
        if api_root in discovery.api_roots:
            discovery.api_roots.remove(api_root)
            discovery.save()
        api_root.delete()
        return redirect('api_roots')
    except Exception as e:
        return error(request, str(e))


@admin_required
def get_collections(request):
    try:
        api_root_name = request.GET['api_root_name']
        api_root = ApiRoot.objects.get(name=api_root_name)
        collections = []
        for collection in api_root.collections:
            collections.append(collection.col_id)
        return JsonResponse({'collections': collections})
    except Exception as e:
        return error(request, str(e))


@admin_required
def get_users(request):
    try:
        api_root_name = request.GET['api_root_name']
        api_root = ApiRoot.objects.get(name=api_root_name)
        return JsonResponse({'users': api_root.stip_meta['users'] if 'users' in api_root.stip_meta else []})
    except Exception as e:
        return error(request, str(e))
