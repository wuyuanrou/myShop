from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse

def index(request):
    if 'user_id' in request.COOKIES:
        return render(request, '../templates/html/index.html', {'isShow': False})
    else:
        return render(request, '../templates/html/index.html', {'isShow': True})


def about(request):
    if 'user_id' in request.COOKIES:
        return render(request, '../templates/html/about.html', {'isShow': False})
    else:
        return render(request, '../templates/html/about.html', {'isShow': True})


def login_page(request):
    return render(request, '../templates/html/login.html')


def register_page(request):
    return render(request, '../templates/html/register.html')

