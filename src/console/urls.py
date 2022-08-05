from django.conf.urls import include
try:
    from django.conf.urls import url as _url
except ImportError:
    from django.urls import re_path as _url
from console.discovery import views as discovery
from console.auth import login, login_totp, logout

urlpatterns = [
    _url(r'^$', discovery.top_redirect),
    _url(r'^logout/$', logout, name='logout'),
    _url(r'^login/$', login, name='login'),
    _url(r'^login_totp/$', login_totp, name='login_totp'),
    _url(r'^discovery/', include('console.discovery.urls')),
    _url(r'^api_roots/', include('console.api_root.urls')),
    _url(r'^collections/', include('console.collection.urls')),
]
