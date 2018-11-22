import os
from django.db import models
from django.dispatch import receiver
from django.conf import settings


class SingleFileUpload(models.Model):
    def loc_func(self, filename):
        return os.path.join(settings.CLOUD_DIR, self.username, self.file_path, self.file.name)
    file_path = models.CharField(max_length=1000)
    file = models.FileField(upload_to=loc_func, max_length=1000, default=None)
    md5sum = models.CharField(max_length=200)
    md5sum_o = models.CharField(max_length=200)
    file_url = models.CharField(max_length=200)
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=200)

    class Meta:
        unique_together = (("username", "name", "file_path"), )

    def __str__(self):
        return self.file.name+'@'+self.username+'md5'+self.md5sum


@receiver(models.signals.post_delete, sender=SingleFileUpload)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    print(instance.file)
    try:
        if instance.file:
            if os.path.isfile(instance.file_url):
                os.remove(instance.file_url)
                filedir = os.path.split(instance.file_url)[0]
                if not os.listdir(filedir):
                    os.rmdir(filedir)
    except IOError as e:
        pass

@receiver(models.signals.pre_save, sender=SingleFileUpload)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = SingleFileUpload.objects.get(pk=instance.pk).file
    except SingleFileUpload.DoesNotExist:
        return False

    new_file = instance.file
    if old_file:
        if not old_file == new_file:
            if os.path.isfile(old_file.file_url):
                os.remove(old_file.file_url)
