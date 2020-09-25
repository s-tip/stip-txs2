from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<status_id>[0-9a-fA-F-]+)/$', views.status),
]
