# Generated by Django 2.1.2 on 2018-10-19 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0005_auto_20181019_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='singlefileupload',
            name='file_name',
            field=models.CharField(default='anon', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='singlefileupload',
            name='file_url',
            field=models.CharField(default='anon', max_length=200),
            preserve_default=False,
        ),
    ]
