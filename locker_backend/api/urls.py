from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .health_check_view import health_check
from .otp_view_set import PasswordItemsOTPViewSet
from .password_items_view_set import PasswordItemsViewSet
from .groups_view_set import GroupsViewSet
from .user_view_set import MyTokenObtainPairView, RegisterView
from .password_history_view_set import PasswordHistoryViewSet

router = routers.SimpleRouter()
otp_router = routers.SimpleRouter()
otp_router.register(r'password-items-otp', PasswordItemsOTPViewSet, basename='password-items-otp')

router.register(r'groups', GroupsViewSet, basename='groups')
router.register(r'password-items', PasswordItemsViewSet, basename='password-items')
router.register(r'password-history', PasswordHistoryViewSet, basename='password-history')

pass_router = routers.NestedSimpleRouter(router, r'groups', lookup='groups')
pass_router.register(r'password-items', PasswordItemsViewSet, basename='groups-password-item')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(pass_router.urls)),
    path(r'', include(otp_router.urls)),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('password-history/<int:pass_id>/', PasswordHistoryViewSet.as_view({'get': 'retrieve'}), name='password-history-detail'),  # Add this line for detail view
    path('health/', health_check, name='health_check'),  # Add health check endpoint

]
