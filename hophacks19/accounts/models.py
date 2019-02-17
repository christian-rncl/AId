from django.db import models
from django.contrib import auth
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    score = models.IntegerField(null=True)

    def __str__(self):
        return "@{}".format(self.username)


class Merchant(models.Model):
    name = models.CharField(max_length=255)
    phone = models.IntegerField()
    category = models.CharField(max_length=255)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return "@{}".format(self.name)
