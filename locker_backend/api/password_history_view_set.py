from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from api.models import PasswordHistory
from api.serializers import PasswordHistorySerializer
from rest_framework.response import Response

class PasswordHistoryViewSet(viewsets.ModelViewSet):
    queryset = PasswordHistory.objects.all()
    serializer_class = PasswordHistorySerializer
    permission_classes = [IsAuthenticated]

@action(methods=['post'], detail=True)
def send_password_to_history(self, request, dataS, groups_pk = None):
    serializer = PasswordHistorySerializer(data=dataS)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
