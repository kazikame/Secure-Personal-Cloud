from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, FileUploadParser, MultiPartParser
from rest_framework import status, viewsets
from .serializers import FileSerializer, UserSerializer
from Authentication.models import SpcUser
import os
from SPC import settings
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = SpcUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class FileView(APIView):
    parser_classes = (MultiPartParser, )

    def post(self, request, *args, **kwargs):
        request.data['username'] = request.user.username
        request.data['file_url'] = os.path.join(settings.CLOUD_DIR, request.user.username, request.data['file_path'], str(request.data['file']))
        print(request.data)
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            #post.user = request.user.username
            #post.file_url = os.path.join(settings.CLOUD_DIR, post.user, post.file_path, str(post.file))
            #post.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)