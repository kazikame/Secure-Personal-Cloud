# Generated by Django 2.1.2 on 2018-11-22 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UploadDownload', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='singlefileupload',
            name='md5sum_o',
            field=models.CharField(default='asdasd', max_length=200),
            preserve_default=False,
        ),
    ]
