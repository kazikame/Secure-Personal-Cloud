from django.conf.urls import re_path, include
from .views import FileView
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    re_path(r'^get_key/$', GetEncryptionKey.as_view(), name='get-key'),
    re_path(r'^set_key/$', SetEncryptionKey.as_view(), name='set-key'),
    re_path(r'^upload/$', FileView.as_view(), name='file-upload'),
    re_path(r'^delete/$', DeleteFile.as_view(), name='file-delete'),
    re_path(r'^download/$', DownloadFile.as_view(), name='file-download'),
    re_path(r'^get-index/$', FileIndex.as_view(), name='file-index'),
    re_path(r'', include('rest_auth.urls')),
]
