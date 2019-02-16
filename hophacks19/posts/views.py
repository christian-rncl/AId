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

User = get_user_model()


class PostList(generic.ListView):
    model = models.Post


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    fields = ("message", "amount", "disaster")
    model = models.Post
    success_url = "/posts/all"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

