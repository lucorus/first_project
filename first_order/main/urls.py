from .views import *
from django.urls import path

urlpatterns = [
    path('', main_page, name='main_page'),
    path('logout', user_logout, name='logout_user'),
    path('register', register, name='register'),
    path('profile/<slug:slug>', profile, name='profile'),
    path('create_history', create_history, name='create_history'),
    path('histories/', histories, name='histories'),
    path('edit_profile/<slug:slug>', edit_profile, name='edit_profile'),
    path('LevelUp/<slug:slug>/<int:level>', up_level, name='LevelUp'),
    path('password/', ChangePasswordView.as_view()),
    path('histories/<int:pk>', histories_with_filter, name='historiesF'),
]
