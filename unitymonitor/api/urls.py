from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path('profiles', views.api_profile_result),
]