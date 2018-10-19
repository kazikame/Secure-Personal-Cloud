from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import SpcUser


class SpcUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = SpcUser
        fields = ('username', 'email')


class SpcUserChangeForm(UserChangeForm):

    class Meta:
        model = SpcUser
        fields = ('username', 'email')

