from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from models import *
from forms import *

@ensure_csrf_cookie
def home(request):
    return render(request, 'home.html')

def register(request):
    user = User()
    form = UserForm(request.POST, instance=user)
    if not form.is_valid():
        return HttpResponse('invalid')
    form.save()
    return HttpResponse('success')
