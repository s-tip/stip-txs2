import django.contrib.auth
from django.shortcuts import render


def admin_required(f):
    def wrap(request, *args, **kwargs):
        stip_user = request.user
        if not stip_user.is_authenticated():
            return render(request, 'cover.html')
        if not stip_user.is_admin:
            django.contrib.auth.logout(request)
            return render(request, 'cover.html')
        return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
