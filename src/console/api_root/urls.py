try:
    from django.conf.urls import url as _url
except ImportError:
    from django.urls import re_path as _url
from . import views

urlpatterns = [
    _url(r'^$', views.api_roots, name='api_roots'),
    _url(r'^create_modify/$', views.create_modify, name='create_modify_api_root'),
    _url(r'^delete/$', views.delete, name='delete_api_root'),
    _url(r'^get_collections/$', views.get_collections),
    _url(r'^get_users/$', views.get_users),
]
