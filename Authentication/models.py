from django.contrib.auth.models import AbstractUser
from lock_tokens.models import LockableModel
from django.db import models


class SpcUser(AbstractUser, LockableModel):

    def __str__(self):
        return self.email
