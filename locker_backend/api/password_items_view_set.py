from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import PasswordItems
from api.serializers import PasswordItemSerializer




class PasswordItemsViewSet(viewsets.ModelViewSet):
    queryset = PasswordItems.objects.all()
    serializer_class = PasswordItemSerializer


    @action(methods=['get'], detail=True)
    def get_password_items(self, request):
        password_items = PasswordItems.objects.all()
        serializer = PasswordItemSerializer(password_items, many=True)
        return Response(serializer.data)


    @action(methods=['post'], detail=True)
    def create_password_item(self, request):
        serializer = PasswordItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    @action(methods=['get'], detail=True)
    def get_specific_password_items(request, pk):
        try:
            user = PasswordItems.objects.get(pk=pk)
        except PasswordItems.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PasswordItemSerializer(user)
        return Response(serializer.data)

    @action(methods=['put'], detail=True)
    def put_password_items(request, pk):
        try:
            user = PasswordItems.objects.get(pk=pk)
        except PasswordItems.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PasswordItemSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], detail=True)
    def delete_password_items(request, pk):
        try:
            user = PasswordItems.objects.get(pk=pk)
        except PasswordItems.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.delete()
