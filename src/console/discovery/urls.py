from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.top, name='discovery'),
    url(r'^modify/$', views.modify, name='modify_discovery'),
]
