from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.view_files, name='browse'),
]