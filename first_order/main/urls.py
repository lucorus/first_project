from .views import *
from django.urls import path

urlpatterns = [
    path('', main_page, name='main_page'),
    path('logout', user_logout, name='logout_user'),
    path('register', register, name='register'),
    path('/profile/<slug:slug>', profile, name='profile'),
    path('create_history', create_history, name='create_history'),
]
