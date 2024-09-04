from django.urls import path
# from .views import get_users, create_user, user_detail, get_passwords
from .views import check, get_passwords, create_password, password_details

urlpatterns = [
    # path('users/', get_users, name='get_users'),
    # path('users/create', create_user, name='create_user'),
    # path('users/<int:pk>', user_detail, name='user_detail'),
    # path('password/', get_passwords, name='get_passwords')
    path('', check, name='check'),
    path('passwords/', get_passwords, name='get_passwords'),
    path('passwords/create/', create_password, name='create_password'),
    path('passwords/<int:pk>/', password_details, name='password_details')

]