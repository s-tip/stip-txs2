import json
from django.shortcuts import render, redirect
from discovery.models import Discovery
from console.error.views import error
from console.decorators import admin_required


@admin_required
def top(request):
    try:
        discovery = Discovery.objects.limit(1)[0]
        return render(
            request,
            'discovery.html',
            {
                'discovery': discovery
            })
    except Exception as e:
        return error(request, str(e))


@admin_required
def top_redirect(request):
    return redirect('discovery')


@admin_required
def modify(request):
    try:
        data = json.loads(request.POST['data'])
        title = data['title']
        description = data['description']
        contact = data['contact']
        default = data['default']
        Discovery.update_or_create(title, description, contact, default)
        return redirect('discovery')
    except Exception as e:
        return error(request, str(e))
