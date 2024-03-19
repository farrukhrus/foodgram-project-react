from django.contrib.auth.models import AbstractUser
from django.db import models as dbmodels


class User(AbstractUser):
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']
    USERNAME_FIELD = 'email'
    email = dbmodels.EmailField(unique=True)
