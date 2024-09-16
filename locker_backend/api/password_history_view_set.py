from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.models import PasswordHistory, decrypt_password
from api.serializers import PasswordHistorySerializer
from rest_framework.response import Response
from rest_framework.exceptions import APIException

class PasswordHistoryViewSet(viewsets.ModelViewSet):
    queryset = PasswordHistory.objects.all()
    serializer_class = PasswordHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(passId__userId=user)  # Filter by user if needed

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = PasswordHistorySerializer(queryset, many=True)

            # Decrypt the passwords before returning the response
            for item in serializer.data:
                try:
                    item['old_passwords'] = decrypt_password(item['old_passwords'])
                except Exception:
                    item['old_passwords'] = "Error decrypting password"

            return Response(serializer.data)
        except Exception as e:
            # Raise an APIException for any errors encountered
            raise APIException("An error occurred while processing your request.")
