from django.contrib.auth.models import AbstractUser
from django.db import models
from lock_tokens.models import LockableModel


class SpcUser(AbstractUser, LockableModel):
    encryptionKey = models.CharField(max_length=200, default="")
    encryptionType = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.email
