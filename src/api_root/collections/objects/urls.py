try:
    from django.conf.urls import url as _url
except ImportError:
    from django.urls import re_path as _url

from . import views as views
from core.response import not_found

urlpatterns = [
    _url(r'(?P<object_id>[0-9a-zA-Z-]+)/versions/$', views.versions),
    _url(r'(?P<object_id>[0-9a-zA-Z-]+)/$', views.object_),
    _url(r'^$', views.objects),
    _url(r'^.+$', not_found),
]
