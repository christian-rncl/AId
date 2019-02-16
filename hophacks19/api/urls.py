from django.urls import path, include
from django.http import HttpResponse
from .views import get_curr_user

app_name = "api"

urlpatterns = [path("<int:username>/", get_curr_user)]

