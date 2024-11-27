from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .is_group_owner_or_read_only import IsGroupOwnerOrReadOnly
from .models import BaseUser, Groups, PasswordItems, PasswordHistory
from .models.invitation import Invitation
from .serializers import GroupsSerializer, InvitationSerializer
from rest_framework.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import send_mail

class GroupsViewSet(viewsets.ModelViewSet):
    queryset = Groups.objects.all()
    serializer_class = GroupsSerializer
    permission_clas = None
    permission_classes = [IsAuthenticated, IsGroupOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        # Filter the groups by the authenticated user
        return Groups.objects.filter(Q(user=user) | Q(invited_members=user)).distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = GroupsSerializer(queryset, many=True)
        return Response(serializer.data)  # No pagination applied

    def send_email_invitation(self, email, group):
        group_pk = group.group_id  # Use the custom primary key field
        subject = f"You've been invited to join the group {group.group_name}"
        message = f"Hello,\n\nYou've been invited to join the group '{group.group_name}'. Please click the link below to accept the invitation:\n\nhttp://127.0.0.1:8000/api/groups/accept-invitation/?email={email}&group_id={group_pk}\n\nThank you!"
        try:
            send_mail(
                subject,
                message,
                'noreply@passwordmanager.com',
                [email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send email to {email}: {e}")

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
        group = self.get_object()
        current_user = request.user

        # Check if the current user is the group owner
        if group.user != current_user:
            raise ValidationError('You do not have permission to invite users to this group.')

        # Get username or email
        username = request.data.get('username')
        email = request.data.get('email')

        if not username and not email:
            raise ValidationError('Please provide either a username or an email.')

        if username:
            # Invite by username
            try:
                invited_user = BaseUser.objects.get(username__iexact=username)
            except BaseUser.DoesNotExist:
                raise ValidationError('The user does not exist.')

            if Invitation.objects.filter(group=group, invited_user=invited_user, accepted=False).exists():
                raise ValidationError('An invitation for this user already exists.')

            # Create an invitation linked to the user
            Invitation.objects.create(group=group, invited_user=invited_user)
            return Response({'message': f'Invitation sent to {username} for group {group.group_name}.'})

        elif email:
            # Validate the email format
            try:
                validate_email(email)
            except ValidationError:
                raise ValidationError('Invalid email format.')

            # Check if the email matches an existing user
            invited_user = BaseUser.objects.filter(email__iexact=email).first()

            if Invitation.objects.filter(group=group, email=email, accepted=False).exists():
                raise ValidationError('An invitation for this email already exists.')

            # Create an invitation, linking the user if found
            Invitation.objects.create(group=group, invited_user=invited_user, email=email)

            # Send an email notification
            self.send_email_invitation(email, group)
            return Response({'message': f'Invitation sent to {email} for group {group.group_name}.'})

    @action(methods=['post'], detail=True, url_path='remove')
    def remove_user(self, request, pk=None):
        group = self.get_object()
        current_user = request.user

        # Ensure the current user is the group owner
        if group.user != current_user:
            raise ValidationError('You do not have permission to remove users from this group.')

        # Accept only username for removing an accepted user
        username_to_remove = request.data.get('username')

        if not username_to_remove:
            raise ValidationError('Provide the username of the user to remove.')

        try:
            # Find the user by username
            user_to_remove = BaseUser.objects.get(username=username_to_remove)

            # Check if the user is a member of the group
            if not group.invited_members.filter(pk=user_to_remove.pk).exists():
                raise ValidationError('This user is not a member of the group.')

            # Remove the user from the group
            group.invited_members.remove(user_to_remove)

        except BaseUser.DoesNotExist:
            raise ValidationError('The user does not exist.')

        return Response({'message': f'User {username_to_remove} has been successfully removed from the group.'})

    @action(methods=['get'], detail=False, url_path='pending-invitations')
    def pending_invitations(self, request):
        invitations = Invitation.objects.filter(invited_user=request.user, accepted=False)
        serializer = InvitationSerializer(invitations, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=False, url_path='accept-invitation')
    def accept_invitation(self, request):
        username = request.user.username  # Automatically use the current user's username
        email = request.data.get('email')  # Optional, for email-based invitations
        group_id = request.data.get('group_id')

        # Validate input
        if not group_id:
            raise ValidationError('group_id is required.')

        try:
            if email:
                # Accept invitation via email
                invitation = Invitation.objects.get(email=email, group__group_id=group_id, accepted=False)
            else:
                # Accept invitation via username
                invitation = Invitation.objects.get(
                    invited_user__username=username, group__group_id=group_id, accepted=False
                )
        except Invitation.DoesNotExist:
            raise ValidationError('No pending invitation found for this user or email.')

        # Add the invited user to the group's invited members
        if invitation.invited_user:
            invitation.group.invited_members.add(invitation.invited_user)

        # Mark the invitation as accepted
        invitation.accepted = True
        invitation.save()

        return Response({'message': f'You have successfully joined the group {invitation.group.group_name}.'})

    @action(methods=['post'], detail=False, url_path='decline-invitation')
    def decline_invitation(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        group_id = request.data.get('group_id')

        # Validate input
        if not group_id or (not username and not email):
            raise ValidationError('group_id and either username or email are required.')

        try:
            # Fetch the invitation based on email or username
            if username:
                invitation = Invitation.objects.get(
                    invited_user__username=username, group__group_id=group_id, accepted=False
                )
            elif email:
                invitation = Invitation.objects.get(
                    email=email, group__group_id=group_id, accepted=False
                )
        except Invitation.DoesNotExist:
            raise ValidationError('No pending invitation found for the provided information.')

        # Delete the invitation
        invitation.delete()

        return Response({'message': 'You have successfully declined the invitation.'})

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
