from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import password_validation
from rest_framework.permissions import AllowAny
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class PasswordResetConfirmView(APIView):
    """
    Handle password reset by verifying the UID and token, and updating the user's password.
    """
    authentication_classes = []  # Disable authentication
    permission_classes = [AllowAny]  # Allow any user (including unauthenticated)

    def post(self, request, uidb64, token):
        try:
            # Decode the user ID from the base64-encoded UID
            uid = urlsafe_base64_decode(uidb64).decode('utf-8')
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, User.DoesNotExist):
            return Response({'detail': 'Invalid reset link'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the token is valid for the user
        if not default_token_generator.check_token(user, token):
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get('new_password')
        if not new_password:
            return Response({'detail': 'New password is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate password (optional, can use Django's built-in password validation)
        try:
            password_validation.validate_password(new_password, user)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Update the user's password
        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Password reset successfully'}, status=status.HTTP_200_OK)
