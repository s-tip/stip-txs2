from django.conf.urls import include, url
from . import views
from core.response import not_found

urlpatterns = [
    url(r'^status/', include(__package__ + '.status.urls')),
    url(r'^collections/', include(__package__ + '.collections.urls')),
    url(r'^$', views.api_root),
    url(r'^.+$', not_found),
]
