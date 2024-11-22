from django.db import models
from django.conf import settings

class Invitation(models.Model):
    group = models.ForeignKey('Groups', on_delete=models.CASCADE, related_name='invitations')
    invited_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invitations', null=True, blank=True
    )
    email = models.EmailField(null=True, blank=True)  # Add email field
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invitation to {self.email or self.invited_user} for group {self.group.group_name}"

