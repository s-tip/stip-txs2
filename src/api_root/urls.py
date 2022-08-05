from django.conf.urls import include
try:
    from django.conf.urls import url as _url
except ImportError:
    from django.urls import re_path as _url
from . import views
from core.response import not_found

urlpatterns = [
    _url(r'^status/', include(__package__ + '.status.urls')),
    _url(r'^collections/', include(__package__ + '.collections.urls')),
    _url(r'^$', views.api_root),
    _url(r'^.+$', not_found),
]
