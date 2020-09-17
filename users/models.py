from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(('email address'),
                              max_length=254,
                              blank=False,
                              null=False,
                              unique=True,
                              )
