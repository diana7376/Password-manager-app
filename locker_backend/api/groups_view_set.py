from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.models import Groups
from api.serializers import GroupsSerializer


class GroupsViewSet(viewsets.ModelViewSet):
    queryset = Groups.objects.all()
    serializer_class = GroupsSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter the groups by the authenticated user
        return Groups.objects.filter(user_id=self.request.user)

    @action(methods=['get'], detail=False)
    def get_groups(self, request):
        groups = self.get_queryset()  # Retrieve only the groups for the authenticated user
        serializer = GroupsSerializer(groups, many=True)
        return Response(serializer.data)


    @action(methods=['post'], detail=True)
    def create_groups(self, request):
        serializer = GroupsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    @action(methods=['get'], detail=True)
    def get_specific_groups(self, request, pk=None):
        queryset = Groups.objects.filter()
        groups = get_object_or_404(queryset, pk=pk)
        serializer = GroupsSerializer(groups)
        return Response(serializer.data)

    @action(methods=['put'], detail=True)
    def put_groups(self, request, pk = None):
        queryset = Groups.objects.filter()
        groups = get_object_or_404(queryset, pk=pk)

        serializer = GroupsSerializer(groups,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], detail=True)
    def delete_groups(self, request, pk = None):
        queryset = Groups.objects.filter()
        groups = get_object_or_404(queryset, pk=pk)

        groups.delete()
