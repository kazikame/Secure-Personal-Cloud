from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class SpcUser(AbstractUser):

    def __str__(self):
        return self.email
