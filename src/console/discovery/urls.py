try:
    from django.conf.urls import url as _url
except ImportError:
    from django.urls import re_path as _url
from . import views

urlpatterns = [
    _url(r'^$', views.top, name='discovery'),
    _url(r'^modify/$', views.modify, name='modify_discovery'),
]
