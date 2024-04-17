from django.urls import path
from . import views

urlpatterns = [
    path('join', views.index, name='index'),
    path('join_result', views.join_result, name='join_result'),
    path('login', views.login, name='login'),
    path('login_result', views.login_result, name='login_result'),
]