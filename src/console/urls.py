from django.conf.urls import include, url
from console.discovery import views as discovery
from console.auth import login, login_totp, logout

urlpatterns = [
    url(r'^$', discovery.top_redirect),
    url(r'^logout/$', logout, name='logout'),
    url(r'^login/$', login, name='login'),
    url(r'^login_totp/$', login_totp, name='login_totp'),
    url(r'^discovery/', include('console.discovery.urls')),
    url(r'^api_roots/', include('console.api_root.urls')),
    url(r'^collections/', include('console.collection.urls')),
]
