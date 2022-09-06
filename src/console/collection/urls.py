try:
    from django.conf.urls import url as _url
except ImportError:
    from django.urls import re_path as _url
from . import views

urlpatterns = [
    _url(r'^$', views.collections, name='collections'),
    _url(r'^create_modify/$', views.create_modify, name='create_modify_collection'),
    _url(r'^delete/$', views.delete, name='delete_collection'),
    _url(r'^generate_uuid/$', views.generate_uuid),
    _url(r'^get_access_authority/$', views.get_access_authority),
]
