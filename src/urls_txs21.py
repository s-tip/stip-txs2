from django.conf.urls import include
try:
    from django.conf.urls import url as _url
except ImportError:
    from django.urls import re_path as _url
from discovery import views as discovery_views
from core.response import not_found

urlpatterns = [
    _url(r'^taxii2/$', discovery_views.discovery),
    _url(r'^(?P<api_root_name>[0-9a-zA-Z_]+?)/', include('api_root.urls')),
    _url(r'^.*$', not_found),
]
