from django.urls import path
from .views import get_users, create_user, user_detail, get_passwords

urlpatterns = [
    path('users/', get_users, name='get_users'),
    path('users/create', create_user, name='create_user'),
    path('users/<int:pk>', user_detail, name='user_detail'),
    path('password/', get_passwords, name='get_passwords')
]