import traceback
from django.shortcuts import render


def error(request, e):
    traceback.print_exc()
    e = {'txt': 'A system error has occurred. Please check the system log.'}
    return render(request, 'error.html', {'error': e})
