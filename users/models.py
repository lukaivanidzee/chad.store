from django.db import models
from django.contrib.auth.models import AbstractUser
from config.model_utiles.models import TieStampModel

class User(AbstractUser, TieStampModel):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(unique=True, max_length=32)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email