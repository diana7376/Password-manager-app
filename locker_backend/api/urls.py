from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .password_items_view_set import PasswordItemsViewSet
from .groups_view_set import GroupsViewSet
from .user_view_set import MyTokenObtainPairView, RegisterView

"""
Our endpoints:

/password_items/unlisted/                   - GET all the password-items with an unlisted group
/password-items/                            - GET all the password-items
/groups/                                    - GET all groups, POST (create) groups
/groups/{pk}/                               - GET a specific group, PUT (update) a specific group, DELETE a specific group
/groups/{groups_pk}/password-items/         - GET all pass-items, POST (create) pass-items
/groups/{groups_pk}/password-items/{pk}/    - GET a spec. pass-items, PUT (update) spec. pass-items, DELETE spec. pass-items
"""

router = routers.SimpleRouter()
router.register(r'groups', GroupsViewSet, basename='groups')
router.register(r'password-items', PasswordItemsViewSet, basename='password-items')
pass_router = routers.NestedSimpleRouter(router, r'groups', lookup='groups')
pass_router.register(r'password-items', PasswordItemsViewSet, basename='groups-password-item')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(pass_router.urls)),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
]

