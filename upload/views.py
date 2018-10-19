from django.shortcuts import render,redirect

# Create your views here.
from .forms import UploadFileForm


def NewUpload(request):
    currentUser = request.user
    if request.method == "POST" :
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = currentUser.username
            post.file_url = post.file_name
            post.save()
            return redirect('home')
    else :
        form = UploadFileForm()
    return render(request,'upload_test.html',{'form' : form})