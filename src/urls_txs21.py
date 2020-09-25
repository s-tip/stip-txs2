from django.conf.urls import include, url
from discovery import views as discovery_views

urlpatterns = [
    url(r'^taxii2/$', discovery_views.discovery),
    url(r'^(?P<api_root_name>[0-9a-zA-Z_]+?)/', include('api_root.urls')),
]
