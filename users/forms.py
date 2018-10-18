from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class SpcUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = SpcUser
        fields = ('username', 'email', 'password')


class SpcUserChangeForm(UserChangeForm):

    class Meta:
        model = SpcUser
        fields = ('username', 'email', 'password')
