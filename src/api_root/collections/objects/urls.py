from django.conf.urls import url
from . import views as views
from core.response import not_found

urlpatterns = [
    url(r'(?P<object_id>[0-9a-zA-Z-]+)/versions/$', views.versions),
    url(r'(?P<object_id>[0-9a-zA-Z-]+)/$', views.object_),
    url(r'^$', views.objects),
    url(r'^.+$', not_found),
]
