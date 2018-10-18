from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import *
from .forms import *

# Register your models here.


class SpcUserAdmin(UserAdmin):
    add_form = SpcUserCreationForm
    form = SpcUserChangeForm
    model = SpcUser
    list_display = ['email', 'username']


admin.site.register(SpcUser, SpcUserAdmin)
