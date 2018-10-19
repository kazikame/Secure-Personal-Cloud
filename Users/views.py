# Users/views.py
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.base import TemplateView

from .forms import SpcUserCreationForm, UploadFileForm


class SignUp(generic.CreateView):
    form_class = SpcUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class UploadFiles(TemplateView):
    form_class = UploadFileForm
    success_url = reverse_lazy('home')
    template_name = 'home.html'

    def post(self, request):
        currentUser = request.user
        form = UploadFileForm(request.POST, request.FILES)
        file = request.FILES['files']
        with open('media/' + currentUser.username +'/testfile', 'wb+') as loc:
            for chunk in file.chunks():
                loc.write(chunk)

