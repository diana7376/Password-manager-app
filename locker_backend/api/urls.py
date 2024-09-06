
from django.urls import path, include
from rest_framework_nested import routers

from .password_items_view_set import PasswordItemsViewSet
from .groups_view_set import GroupsViewSet


router = routers.SimpleRouter()
router.register(r'groups', GroupsViewSet, basename='groups')
#router.register(r'password-items', PasswordItemsViewSet, basename='password-items')

pass_router = routers.NestedSimpleRouter(router, r'groups', lookup='groups')


pass_router.register(r'password-items', PasswordItemsViewSet, basename='groups-password-item')
#router.register(r'groups/{bk}/password-items/{pk}', PasswordItemsViewSet, basename='item')

urlpatterns = router.urls

