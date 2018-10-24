from django.contrib.auth.models import AbstractUser


class SpcUser(AbstractUser):
    def __str__(self):
        return self.email
