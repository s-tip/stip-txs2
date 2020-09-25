import traceback
from django.shortcuts import render


def error(request, e):
    traceback.print_exc()
    e = {'txt': str(e)}
    return render(request, 'error.html', {'error': e})
