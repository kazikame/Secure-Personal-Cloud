from django.urls import path, include
from Authentication import views
from django.views.generic.base import TemplateView
urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
]