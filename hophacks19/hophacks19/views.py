from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from posts.models import Disaster


class HomePage(ListView):
    model = Disaster
    template_name = "index.html"

