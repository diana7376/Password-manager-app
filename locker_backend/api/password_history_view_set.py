from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.models import PasswordHistory, decrypt_password
from api.mypagination import MyPageNumberPagination
from api.serializers import PasswordHistorySerializer
from rest_framework.response import Response
from rest_framework.exceptions import APIException

class PasswordHistoryViewSet(viewsets.ModelViewSet):
    queryset = PasswordHistory.objects.all()
    serializer_class = PasswordHistorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pass_id'  # We're using pass_id instead of pk
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(pass_id__user_id=user)  # Filter by user

    def retrieve(self, request, *args, **kwargs):
        pass_id = kwargs.get('pass_id')
        queryset = self.get_queryset().filter(pass_id=pass_id)

        if not queryset.exists():
            raise APIException(f"No password history found for pass_id: {pass_id}")

        # Apply pagination to the password history
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)

            # Decrypt passwords before returning the response
            data = serializer.data
            for item in data:
                try:
                    item['oldPassword'] = decrypt_password(item['oldPassword'])
                except Exception:
                    item['oldPassword'] = "Error decrypting password"

            # Return paginated response
            return self.get_paginated_response(data)


        serializer = PasswordHistorySerializer(queryset, many=True)

        # Decrypt passwords before returning the response
        data = serializer.data
        for item in data:
            try:
                item['oldPassword'] = decrypt_password(item['oldPassword'])
            except Exception:
                item['oldPassword'] = "Error decrypting password"

        return Response(data)
