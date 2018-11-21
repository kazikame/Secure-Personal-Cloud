from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework import status, viewsets
from .serializers import FileSerializer, UserSerializer
from Authentication.models import SpcUser
from SPC import settings
from .models import *
from django.db.models.base import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import FileResponse
import hashlib
from functools import partial

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
                    file_serializer.save(username=request.user.username,
                                         file_url=os.path.join(settings.CLOUD_DIR,
                                                               request.user.username,
                                                               file_serializer.validated_data['file_path'],
                                                               str(request.data['file'])),
                                         name=request.data['file'].name)
                    instance = file_serializer.save(file=request.data['file'])
                    if os.path.isfile(os.path.abspath(instance.file_url)):
                        f = open(os.path.abspath(instance.file_url), 'rb')
                        md5 = md5sum(f)
                        if md5 != instance.md5sum:
                            instance.delete()
                            return Response({'Error': "MD5 don't match."}, status=status.HTTP_406_NOT_ACCEPTABLE)
                except IntegrityError as e:
                    return Response({'Error': 'File already exists'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'detail': 'Success'}, status=status.HTTP_201_CREATED)
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
                return Response({"error": "User not found!"}, status=status.HTTP_400_BAD_REQUEST)


class DeleteFile(APIView):
    parser_classes = (FormParser, )

    def post(self, request):
        if request.user.is_authenticated:
            try:
                file_path = request.data['file_path'].split('```')
                name_list = request.data['name_list'].split('```')
                print(name_list)
                print(file_path)
                instance = SingleFileUpload.objects.filter(username=request.user.username, file_path__in=file_path, name__in=name_list)
                instance.delete()
                instance.get().delete()
                return Response({'detail': 'Successful!'}, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'detail': 'Unknown Error!'})
        else:
            return Response({'detail': "Authentication credentials were invalid."})


class DownloadFile(APIView):
    parser_classes = (FormParser, )

    def post(self, request):
        if request.user.is_authenticated:
            try:
                dfile_path = request.data['file_path']
                dfile_name = request.data['name']

                instance = SingleFileUpload.objects.filter(username=request.user.username, file_path=dfile_path, name=dfile_name)
                if instance.count() > 0:
                    obj = instance.all()[:1].get()
                    file_url = obj.file_url
                    md5 = obj.md5sum
                    f = open(file_url, 'rb')
                    response = FileResponse(f, filename=dfile_name + '```' + md5, as_attachment=True)
                    return response
                else:
                    return Response({'error': 'file not found'})
            except Exception as e:
                print(e)
                return Response({'error': 'Unknown error'})
        else:
            return Response({'detail': 'Authentication credentials were invalid.'})


class FileIndex(APIView):
    def post(self, request):
        indexSet = list(SingleFileUpload.objects.filter(username=request.user.username).values('file_path', 'name', 'md5sum'))

        index = []
        for i in indexSet:
            index.append({'file_path': i['file_path'] + '/' + i['name'], 'md5sum': i['md5sum']})

        return Response({'index': index})


def md5sum(f):
    d = hashlib.md5()
    for buf in iter(partial(f.read, 128), b''):
        d.update(buf)
    return d.hexdigest()
