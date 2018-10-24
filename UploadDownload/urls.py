from django.conf.urls import re_path, include
from .views import FileView
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    re_path(r'^upload/$', FileView.as_view(), name='file-upload'),
    re_path(r'', include('rest_auth.urls')),
    #re_path(r'^/download/?P<id>+/?P<filepathT>+', FileDownload.as_view(), name='file-download')
]