from django.db import models
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth import get_user_model

User = get_user_model()


class Disaster(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)
    state = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    payer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payer", null=True
    )
    disaster = models.ForeignKey(Disaster, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    received_at = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=255)
    amount = models.IntegerField(null=True)
    category = models.CharField(max_length=255, null=True)
    paid = models.BooleanField(default=False)
    pin = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "message"]

