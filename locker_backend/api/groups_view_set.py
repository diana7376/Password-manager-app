from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .is_group_owner_or_read_only import IsGroupOwnerOrReadOnly
from .models import BaseUser, Groups, PasswordItems, PasswordHistory
from .serializers import GroupsSerializer
from rest_framework.exceptions import ValidationError

class GroupsViewSet(viewsets.ModelViewSet):
    queryset = Groups.objects.all()
    serializer_class = GroupsSerializer
    permission_clas = None
    permission_classes = [IsAuthenticated, IsGroupOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        # Filter the groups by the authenticated user
        return Groups.objects.filter(Q(user=user) | Q(invited_members=user))

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = GroupsSerializer(queryset, many=True)
        return Response(serializer.data)  # No pagination applied

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

    @action(methods=['post'], detail=True, url_path='invite')
    def invite_user(self, request, pk=None):
        group = self.get_object()  # Get the group using the primary key from the URL
        current_user = request.user

        # Check if the current user is the owner of the group
        if group.user != current_user:
            raise ValidationError('You do not have permission to invite users to this group.')

        # Get the username of the user to invite from the request data
        username_to_invite = request.data.get('username')
        if not username_to_invite:
            raise ValidationError('No username provided.')

        # Look up the invited user by username
        try:
            invited_user = BaseUser.objects.get(username__iexact=username_to_invite)
        except BaseUser.DoesNotExist:
            raise ValidationError('The user does not exist.')

        # Check if the user is already invited
        if group.invited_members.filter(user_id=invited_user.user_id).exists():
            raise ValidationError('This user is already invited to the group.')

        # Add the user to the group's invited members
        group.invited_members.add(invited_user)
        return Response({'message': f'User {username_to_invite} has been successfully invited to the group.'})

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
