from django.conf.urls import include
try:
    from django.conf.urls import url as _url
except ImportError:
    from django.urls import re_path as _url
from . import views
from .objects import views as objects_views
from core.response import not_found

urlpatterns = [
    _url(r'(?P<collection_id>[0-9a-zA-Z-_]+)/manifest/$', objects_views.manifest),
    _url(r'(?P<collection_id>[0-9a-zA-Z-_]+)/objects/', include(__package__ + '.objects.urls')),
    _url(r'(?P<collection_id>[0-9a-zA-Z-_]+)/$', views.collection),
    _url(r'^$', views.collections),
    _url(r'^.+$', not_found),
]
