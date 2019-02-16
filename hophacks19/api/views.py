from django.shortcuts import render
from accounts.models import User
from django.http import HttpResponse

# Create your views here.


def get_curr_user(request, username):
    obj = User.objects.filter(username=username).first()
    return HttpResponse(obj != None)
