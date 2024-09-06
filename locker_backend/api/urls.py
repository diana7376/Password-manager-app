from django.urls import path

from .views import get_password_items, create_password_item, get_password_item, update_password_item, delete_password_item


urlpatterns = [
    path('password-items/', get_password_items, name='get_password_items'),
    path('password-items/', create_password_item, name='create_password_item'),
    path('password-items/<int:pk>', get_password_item, name='get_password_item'),
    path('password-items/<int:pk>', update_password_item, name='update_password_item'),
    path('password-items/<int:pk>', delete_password_item, name='delete_password_item'),

]

