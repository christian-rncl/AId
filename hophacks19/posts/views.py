from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic
from braces.views import SelectRelatedMixin
from posts import forms
from posts import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render, get_object_or_404
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from random import randint
import requests
import numpy as np

stripe.api_key = settings.STRIPE_SECRET_KEY
User = get_user_model()


class PostList(generic.ListView):
    model = models.Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["key"] = settings.STRIPE_PUBLISHABLE_KEY
        return context


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    fields = ("message", "amount", "disaster", "category")
    model = models.Post
    success_url = "/posts/all"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ChargeView(generic.TemplateView):
    template_name = "posts/charge.html"


@login_required
def update_post(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    post.paid = True
    post.payer = request.user
    post.pin = str(np.base_repr(pow(post.pk + 1, 65537, 5551201688147), base=36))
    post.save()
    url = "http://d98ae961.ngrok.io/notifyuser"
    json = {"pin": post.pin, "phone": post.user.username, "amount": post.amount}
    requests.post(url, data=json)
    return render(request, "posts/charge.html")


class DeletePost(LoginRequiredMixin, generic.DeleteView):
    model = models.Post
    success_url = reverse_lazy("posts:all")

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)

