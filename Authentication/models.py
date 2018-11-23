from django.contrib.auth.models import AbstractUser
from lock_tokens.models import LockableModel
from django.db import models


class SpcUser(AbstractUser, LockableModel):
    encryptionKey = models.CharField(max_length=200, default="")
    encryptionType = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.email
