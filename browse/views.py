from django.shortcuts import render

# Create your views here.

from upload.models import SingleFileUpload

def view_files(request):
    currentUser = request.user
    files = SingleFileUpload.objects.filter(user=currentUser.username)
    return render(request, 'browse.html', {'files': files})