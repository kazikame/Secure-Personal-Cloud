from django.db import models

# Create your models here.


class SingleFileUpload(models.Model):
    file_path = models.CharField(max_length=100)
    file_name = models.CharField(max_length=100)
    file = models.FileField()
    file_url = models.CharField(max_length=200)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.file_path+'/'+self.file_name+'@'+self.user

