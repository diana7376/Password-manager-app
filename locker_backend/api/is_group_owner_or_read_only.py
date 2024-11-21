from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsGroupOwnerOrReadOnly(BasePermission):
    """
    Custom permission to allow group owners full CRUD access and invited users read-only access.
    """
    def has_object_permission(self, request, view, obj):
        # Allow read-only actions for invited users
        if request.method in SAFE_METHODS:
            # Check if the user is the group owner or an invited member
            return obj.user == request.user or obj.invited_members.filter(user_id=request.user.user_id).exists()

        # Allow full CRUD access only for the group owner
        return obj.user == request.user
