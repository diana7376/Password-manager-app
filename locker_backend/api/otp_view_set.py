from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from django_otp.oath import totp
import time
import base64
from api.models import PasswordItems
from api.models.encryption import decrypt_password
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


class PasswordItemsOTPViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(methods=['post'], detail=True, url_path='update-otp')
    def update_otp_key(self, request, pk=None):
        password_item = get_object_or_404(PasswordItems, pk=pk, user=request.user)

        otp_key = request.data.get('otpKey')
        if not otp_key:
            return Response({'responseKey': 'Secret key is required'}, status=status.HTTP_400_BAD_REQUEST)
        # Trim leading and trailing white spaces
        otp_key = otp_key.replace(" ", "")
        password_item.otp_key = otp_key
        password_item.save_otp_key()
        return Response({'responseKey': 'OTP key updated successfully'}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='generate-otp')
    def get_otp(self, request, pk=None):
        password_item = get_object_or_404(PasswordItems, pk=pk, user=request.user)

        if not password_item.otp_key:
            return Response({'responseKey': 'No OTP key found for this item'}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Decrypt OTP key
            decrypted_key = decrypt_password(password_item.otp_key)

            # Ensure the key is uppercase
            decrypted_key = decrypted_key.upper()

            # Calculate missing padding
            padding_needed = (8 - len(decrypted_key) % 8) % 8  # Padding required to make length a multiple of 8
            decrypted_key += '=' * padding_needed

            # Decode the Base32 key
            base32_key = base64.b32decode(decrypted_key, casefold=True)  # Allow mixed case

            # Generate OTP
            now = int(time.time())
            step = 30
            otp = totp(key=base32_key, step=step, digits=6, t0=0)

            # Ensure OTP is 6 digits
            if len(str(otp)) != 6:
                return Response({'responseKey': 'Failed to generate a valid OTP.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'responseKey': otp}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'responseKey': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['delete'], detail=True, url_path='delete-otp')
    def delete_otp_key(self, request, pk=None):
        # Retrieve the password item
        password_item = get_object_or_404(PasswordItems, pk=pk, user=request.user)

        if not password_item.otp_key:
            return Response({'responseKey': 'No OTP key to delete for this item'}, status=status.HTTP_404_NOT_FOUND)

        # Remove the OTP key
        password_item.otp_key = None
        password_item.save_otp_key()  # Call save_otp_key() to save the updated object

        return Response({'responseKey': 'OTP key deleted successfully'}, status=status.HTTP_200_OK)