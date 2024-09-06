from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import PasswordItems
from api.serializers import PasswordItemSerializer


class PasswordItemsViewSet(viewsets.ModelViewSet):
    queryset = PasswordItems.objects.all()
    serializer_class = PasswordItemSerializer

    @action(methods=['get'], detail=True)
    def get_password_items(self, request, groups_pk = None):
        password_items = PasswordItems.objects.all(groups=groups_pk) #!!
        serializer = PasswordItemSerializer(password_items, many=True)
        return Response(serializer.data)


    @action(methods=['post'], detail=True)
    def create_password_item(self, request, groups_pk = None):
        serializer = PasswordItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['get'], detail=True)
    def get_specific_password_items(self, request, pk = None, groups_pk = None):
        queryset = PasswordItems.objects.filter(pk=pk, groups=groups_pk)
        password_items = get_object_or_404(queryset, pk=pk)
        serializer = PasswordItemSerializer(password_items)
        return Response(serializer.data)

    @action(methods=['put'], detail=True)
    def put_password_items(self, request, pk=None, groups_pk = None):
        queryset = PasswordItems.objects.filter(pk=pk, groups=groups_pk)
        password_items = get_object_or_404(queryset, pk=pk)

        serializer = PasswordItemSerializer(password_items, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], detail=True)
    def delete_password_items(self, request, pk=None, groups_pk = None):
        queryset = PasswordItems.objects.filter(pk=pk, groups=groups_pk)
        password_items = get_object_or_404(queryset, pk=pk)

        password_items.delete()
