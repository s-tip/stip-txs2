try:
    from django.conf.urls import url as _url
except ImportError:
    from django.urls import re_path as _url
from . import views

urlpatterns = [
    _url(r'^(?P<status_id>[0-9a-fA-F-]+)/$', views.status),
]
