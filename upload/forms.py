from django import forms
from .models import SingleFileUpload

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = SingleFileUpload
        fields = ('file_path','file','md5sum',)