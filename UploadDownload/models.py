import os
from django.db import models
from django.dispatch import receiver
from django.conf import settings


class SingleFileUpload(models.Model):
    def loc_func(self, filename):
        return os.path.join(settings.CLOUD_DIR, self.user, self.file_path, str(self.file))
    file_path = models.CharField(max_length=100)
    file = models.FileField(upload_to=loc_func, max_length=1000)
    name = models.CharField(max_length=200)
    md5sum = models.CharField(max_length=200)
    file_url = models.CharField(max_length=200)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.file.name+'@'+self.user+'md5'+self.md5sum


@receiver(models.signals.post_delete, sender=SingleFileUpload)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

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
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
