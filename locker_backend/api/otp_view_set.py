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

        password_item.otp_key = otp_key
        password_item.save()
        return Response({'responseKey': 'OTP key updated successfully'}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='generate-otp')
    def get_otp(self, request, pk=None):
        password_item = get_object_or_404(PasswordItems, pk=pk, user=request.user)

        if not password_item.otp_key:
            return Response({'responseKey': 'No OTP key found for this item'}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Decrypt OTP key and ensure it is Base32 encoded
            decrypted_key = decrypt_password(password_item.otp_key)

            # Fix padding issue with Base32
            decrypted_key = decrypted_key.upper()  # Make sure the key is uppercase
            # Pad the string to ensure it's a multiple of 8 characters for Base32 decoding
            padding = '=' * (8 - len(decrypted_key) % 8)  # Add necessary padding
            decrypted_key += padding

            base32_key = base64.b32decode(decrypted_key)  # Decode the Base32 key

            # Get current time in seconds since Unix epoch
            now = int(time.time())  # This will be the number of seconds since epoch
            step = 30  # OTP step interval in seconds (common value is 30)

            # Generate OTP
            otp = totp(key=base32_key, step=step, digits=6, t0=0)

            # Ensure OTP is 6 digits (if there’s any issue with generation)
            if len(str(otp)) != 6:
                return Response({'responseKey': 'Failed to generate a valid OTP.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'responseKey': otp}, status=status.HTTP_200_OK)

        except Exception as e:
            # If there's any error during decryption or OTP generation, log it and return a response
            return Response({'responseKey': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
