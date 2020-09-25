from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.collections, name='collections'),
    url(r'^create_modify/$', views.create_modify, name='create_modify_collection'),
    url(r'^delete/$', views.delete, name='delete_collection'),
    url(r'^generate_uuid/$', views.generate_uuid),
    url(r'^get_access_authority/$', views.get_access_authority),
]
