from django.urls import path, include
from rest_framework_nested import routers

from .password_items_view_set import PasswordItemsViewSet
from .groups_view_set import GroupsViewSet


"""
Our endpoints:

/password-items/                            - GET all the password-items
/groups/                                    - GET all groups, POST groups
/groups/{pk}/                               - GET a specific group, PUT a specific group, DELETE a specific group
/groups/{groups_pk}/password-items/         - GET all pass-items, POST pass-items
/groups/{groups_pk}/password-items/{pk}/    - GET a specific pass-items, PUT spec. pass-items, DELETE spec. pass-items
"""

router = routers.SimpleRouter()
router.register(r'groups', GroupsViewSet, basename='groups')
router.register(r'password-items', PasswordItemsViewSet, basename='password-items')
pass_router = routers.NestedSimpleRouter(router, r'groups', lookup='groups')
pass_router.register(r'password-items', PasswordItemsViewSet, basename='groups-password-item')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(pass_router.urls)),
]

