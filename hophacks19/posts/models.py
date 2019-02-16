from django.db import models
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    user = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    received_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    amount = models.IntegerField()

    def __str__(self):
        return self.message

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "message"]
