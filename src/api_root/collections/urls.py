from django.conf.urls import url, include
from . import views
from .objects import views as objects_views
from core.response import not_found

urlpatterns = [
    url(r'(?P<collection_id>[0-9a-zA-Z-_]+)/manifest/$', objects_views.manifest),
    url(r'(?P<collection_id>[0-9a-zA-Z-_]+)/objects/', include(__package__ + '.objects.urls')),
    url(r'(?P<collection_id>[0-9a-zA-Z-_]+)/$', views.collection),
    url(r'^$', views.collections),
    url(r'^.+$', not_found),
]
