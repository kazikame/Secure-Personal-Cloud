from django.shortcuts import render,redirect

# Create your views here.
from .forms import UploadFileForm
from .models import SingleFileUpload

def NewUpload(request):
    currentUser = request.user
    if request.method == "POST" :
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = currentUser.username
            post.file_url = post.file.name
            post.name = post.file.name
            if (SingleFileUpload.objects.filter(name=post.name)):
                SingleFileUpload.objects.get(name=post.name).delete()
            post.save()
            return redirect('success')
    else :
        form = UploadFileForm()
    return render(request,'upload_test.html',{'form' : form})

def success(request):
    return render(request,'upload_success.html',{})