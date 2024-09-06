from django.urls import path

from .views import get_post_password_items, get_put_delete_password_items


urlpatterns = [
    path('password-items/', get_post_password_items, name='get_password_items'),
    path('password-items/', get_post_password_items, name='put_password_items'),
    path('password-items/<int:pk>', get_put_delete_password_items, name='get_specific_password_items'),
    path('password-items/<int:pk>', get_put_delete_password_items, name='put_password_items'),
    path('password-items/<int:pk>', get_put_delete_password_items, name='delete_password_item'),

]

