from django.urls import path
from Authentication import views
from django.views.generic.base import TemplateView
urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
]