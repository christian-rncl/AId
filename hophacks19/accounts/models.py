from django.db import models
from django.contrib import auth
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    score = models.IntegerField(default=5)

    def __str__(self):
        return "@{}".format(self.username)

