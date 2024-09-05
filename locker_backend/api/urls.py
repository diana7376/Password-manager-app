from django.urls import path

from .views import get_password_items, create_password_item, password_item_details


urlpatterns = [
    path('password-item/', get_password_items, name='get_password_items'),
    path('password-item/', create_password_item, name='create_password_item'),
    path('password-item/<int:pk>', password_item_details, name='password_item_details'),

]

