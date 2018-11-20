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
                                                               request.data['filename']),
                                         name=request.data['filename'])
                    print(request.FILES)
                    file_serializer.save(file=request.FILES['file'])
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
                return Response({"error": "User not found!"}, status=status.HTTP_400_BAD_REQUEST)


class DeleteFile(APIView):
    parser_classes = (FormParser, )

    def post(self, request):
        if request.user.is_authenticated:
            try:
                file_path = request.data['file_path'].split(',')
                md5 = request.data['md5sum'].split(',')
                print(md5)
                print(file_path)
                instance = SingleFileUpload.objects.filter(username=request.user.username, file_path__in=file_path, md5sum__in=md5)
                if instance.count() > 0:
                    instance.delete()
                else:
                    return Response({'error': 'No such files exist.'})
                return Response({'detail': 'Successful!'})
            except Exception as e:
                print(e)
                return Response({'detail': 'Unknown Error!'})
        else:
            return Response({'detail': "Authentication credentials were invalid."})


class FileIndex(APIView):
    def post(self, request):
        indexSet = list(SingleFileUpload.objects.filter(username=request.user.username).values('file_path', 'name', 'md5sum'))

        index = []
        for i in indexSet:
            index.append({'file_path': i['file_path'] + '/' + i['name'], 'md5sum': i['md5sum']})

        return Response({'index': index})

