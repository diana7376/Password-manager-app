from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.groups_view_set import GroupsViewSet
from api.models import PasswordItems, Groups
from api.serializers import PasswordItemSerializer


class PasswordItemsViewSet(viewsets.ModelViewSet):
    serializer_class = PasswordItemSerializer
## Filtering the proper queryset based on the group_pk from url
    def get_queryset(self):
        try:
            group_id = self.kwargs['groups_pk']
            return PasswordItems.objects.filter(groupId=group_id)
        except KeyError:
            return PasswordItems.objects.all()

    @action(methods=['get'], detail=False)
    def get_password_items_by_location(self, request, groups_pk=None):
        group_location = self.request.query_params.get('group_location')
        if group_location is not None:
            password_items = PasswordItems.objects.filter(
                groupId__groupId=groups_pk,
                groupId__groupName=group_location
            )
            serializer = PasswordItemSerializer(password_items, many=True)
            return Response(serializer.data)
        return Response({"detail": "Group location not provided"}, status=status.HTTP_400_BAD_REQUEST)

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
