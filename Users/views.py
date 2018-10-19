# Users/views.py
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.base import TemplateView

from .forms import SpcUserCreationForm


class SignUp(generic.CreateView):
    form_class = SpcUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'