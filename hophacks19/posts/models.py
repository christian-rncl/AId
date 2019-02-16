from django.db import models
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth import get_user_model

User = get_user_model()


class Disaster(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disaster = models.ForeignKey(Disaster, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    received_at = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=255)
    amount = models.IntegerField()

    def __str__(self):
        return self.message

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "message"]

