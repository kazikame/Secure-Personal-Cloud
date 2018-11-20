from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, FileUploadParser, MultiPartParser
from rest_framework import status, viewsets
from .serializers import FileSerializer, UserSerializer
from Authentication.models import SpcUser
from SPC import settings
from .models import *
from django.db.models.base import ObjectDoesNotExist
from django.db import IntegrityError
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = SpcUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        if request.user.is_authenticated:
            file_serializer = FileSerializer(data=request.data)
            if file_serializer.is_valid():
                try:
                    file_serializer.save(file=request.FILES['file'], username=request.user.username,
                                         file_url=os.path.join(settings.CLOUD_DIR,
                                                               request.user.username,
                                                               file_serializer.validated_data['file_path'],
                                                               request.data['filename']))
                except IntegrityError as e:
                    return Response({'Error':'File already exists'}, status=status.HTTP_400_BAD_REQUEST)
                return Response(file_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(file_serializer.errors, status=status.HTTP_403_FORBIDDEN)


class GetEncryptionKey(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            try:
                user_details = SpcUser.objects.get(username=request.user.username)
                return Response({"key": user_details.encryptionKey, "type": user_details.encryptionType})
            except ObjectDoesNotExist:
                return Response({"detail": "User not found!"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "You are not logged in :("}, status=status.HTTP_403_FORBIDDEN)


class SetEncryptionKey(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            try:
                user_details = SpcUser.objects.get(username=request.user.username)
                if ('type' in request.POST) and ('key' in request.POST):
                    user_details.encryptionType = request.POST['type']
                    user_details.encryptionKey = request.POST['key']
                    user_details.save()
                    return Response({"detail": "Accepted!"}, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({"detail": "Incorrect arguments provided"}, status=status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist:
                return Response({"detail": "User not found!"}, status=status.HTTP_400_BAD_REQUEST)

