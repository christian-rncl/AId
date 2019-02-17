from django.shortcuts import render, get_object_or_404
from accounts.models import User, Merchant
from posts.models import Post, Disaster
from django.http import HttpResponse
from django.core import serializers
import numpy as np
import requests

# Create your views here.


def get_curr_user(request, username):
    try:
        obj = User.objects.get(username=username)
    except User.DoesNotExist:
        u = User(username=username)
        u.save()
        obj = u
    return HttpResponse(serializers.serialize("json", [obj]))


def update_first(request, username, first_name):
    user = User.objects.get(username=username)
    user.first_name = first_name
    user.save()
    return HttpResponse(serializers.serialize("json", [user]))


def update_last(request, username, last_name):
    user = User.objects.get(username=username)
    user.last_name = last_name
    user.save()
    return HttpResponse(serializers.serialize("json", [user]))


def create_post(request, username, message):
    post = Post(message=message)
    post.user = User.objects.get(username=username)
    post.save()
    return HttpResponse(serializers.serialize("json", [post]))


def update_disaster(request, username, pk):
    user = User.objects.get(username=username)
    post = Post.objects.filter(user=user).first()
    post.disaster = Disaster.objects.get(pk=pk)
    post.save()
    return HttpResponse(serializers.serialize("json", [post]))


def update_amount(request, username, amount):
    user = User.objects.get(username=username)
    post = Post.objects.filter(user=user).first()
    post.amount = amount
    post.save()
    return HttpResponse(serializers.serialize("json", [post]))


def get_disasters(request):
    return HttpResponse(serializers.serialize("json", Disaster.objects.all()))


def update_category(request, username, category):
    user = User.objects.get(username=username)
    post = Post.objects.filter(user=user).first()
    post.category = category
    post.save()
    return HttpResponse(serializers.serialize("json", [post]))


def make_transaction(request, merchant_phone, pk):
    try:
        merchant = Merchant.objects.get(phone=merchant_phone)
    except Merchant.DoesNotExist:
        return HttpResponse("No such merchant")
    pk = pow(int(np.base_repr(int(pk, 36), base=10)), 109182490673, 5551201688147) - 1
    obj = Post.objects.get(pk=pk)
    merchant.balance += obj.amount
    merchant.save()
    user = obj.user
    user.transactions += 1
    user.save()
    return HttpResponse(serializers.serialize("json", [user]))


def update_score(request, username, cat):
    user = User.objects.get(username=username)
    post = Post.objects.filter(user=user).first()
    if post.category == cat:
        user.thumb_ups += 1
        user.save()
    return HttpResponse(serializers.serialize("json", [user]))
