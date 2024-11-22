from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from rest_framework.permissions import AllowAny
import logging
import os

User = get_user_model()
logger = logging.getLogger(__name__)

class PasswordResetRequestView(APIView):
    authentication_classes = []  # Disable authentication
    permission_classes = [AllowAny]  # Allow unauthenticated users

    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({'detail': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)

        uid = urlsafe_base64_encode(str(user.pk).encode('utf-8'))
        token = default_token_generator.make_token(user)

        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
        reset_link = f"{frontend_url}/reset/{uid}/{token}/"

        email_subject = "Password Reset Request"
        email_body = f"""
        Hi {user.username},

        We received a request to reset your password. Click the link below to proceed:
        {reset_link}

        If you did not request this, you can safely ignore this email.

        Thanks,
        LockR Team
        """

        # Retrieve API key and validate
        api_key = os.getenv('SENDGRID_API_KEY')
        if not api_key:
            logger.error("SendGrid API key is missing")
            return Response(
                {'detail': 'Email service configuration error. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Send the email
        try:
            message = Mail(
                from_email='wexow66243@kazvi.com',  # Replace with verified sender email
                to_emails=email,
                subject=email_subject,
                plain_text_content=email_body,
            )
            sg = SendGridAPIClient(api_key)
            response = sg.send(message)

            if response.status_code != 202:
                logger.error(f"Failed to send email. Status: {response.status_code}, Body: {response.body}")
                return Response(
                    {'detail': 'Error sending email. Please try again later.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            logger.info(f"Password reset email sent to {email}. Status: {response.status_code}")
        except Exception as e:
            logger.error(f"Error sending password reset email: {e}")
            return Response(
                {'detail': 'Error sending email. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({'detail': 'Password reset email sent.'}, status=status.HTTP_200_OK)
