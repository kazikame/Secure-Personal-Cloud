# Generated by Django 2.1.2 on 2018-10-19 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spcuser',
            name='files',
        ),
    ]
