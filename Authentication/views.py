from django.urls import reverse_lazy
from django.views import generic
from .forms import SpcUserCreationForm


class SignUp(generic.CreateView):
    form_class = SpcUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
