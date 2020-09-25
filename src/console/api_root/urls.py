from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.api_roots, name='api_roots'),
    url(r'^create_modify/$', views.create_modify, name='create_modify_api_root'),
    url(r'^delete/$', views.delete, name='delete_api_root'),
    url(r'^get_collections/$', views.get_collections),
    url(r'^get_users/$', views.get_users),
]
