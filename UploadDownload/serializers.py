from UploadDownload.models import SingleFileUpload
from rest_framework import serializers
from Authentication.models import SpcUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SpcUser
        fields = ('username', 'email', 'url')


class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SingleFileUpload
        fields = ('file_path', 'md5sum', 'md5sum_o')
