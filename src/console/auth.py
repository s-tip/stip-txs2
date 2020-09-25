import django.contrib.auth
from django.shortcuts import redirect
import stip.common.login as login_views
from console.decorators import admin_required

REDIRECT_TO = 'discovery'


def login(request):
    return login_views.login(request, REDIRECT_TO)


def login_totp(request):
    return login_views.login_totp(request, REDIRECT_TO)


@admin_required
def logout(request):
    django.contrib.auth.logout(request)
    return redirect('discovery')
