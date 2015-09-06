from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from models import *
from forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
import json


@ensure_csrf_cookie
def home(request):
    return render(request, 'home.html')

def register(request):
    user = User()
    form = UserForm(request.POST, instance=user)
    print('PAST USER FORM')
    if not form.is_valid():
        print('INVALID FORM')
        return HttpResponse('invalid')
    try:
        print('TRYING TO GET USER')
        User.objects.get(user_id=form.cleaned_data['user_id'])
    except ObjectDoesNotExist:
        PRINT("DNEDNEDNE")
        form.save()
        return HttpResponse('success')
    return HttpResponse('existing user')

def get_messages(request):
    try:
        print('asdfsdf')
        print(request.GET.get('user_id'))
        user = User.objects.get(user_id=request.GET.get('user_id'))
    except ObjectDoesNotExist:
        return HttpResponse('user does not exist')

    return JsonResponse(user.messages)
    #messages_serialized = serializers.serialize('json', user.messages, safe=False)
    #return JsonResponse(messages_serialized)
    #return HttpResponse(JsonResponse(json.loads(posts_serialized), safe=False) , content_type="application/json")
