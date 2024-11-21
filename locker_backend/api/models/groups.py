from django.db import models
from .base_user import BaseUser  # Adjust the import according to your project structure
from rest_framework.exceptions import ValidationError

class Groups(models.Model):
    group_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="groups")
    group_name = models.CharField(max_length=100, unique=True)
    invited_members = models.ManyToManyField(
        BaseUser,
        related_name='shared_groups',
        blank=True,
    )

    class Meta:
        db_table = 'groups'

    def __str__(self):
        return self.group_name

    def save(self, *args, **kwargs):
        if self.user:
            try:
                existing_group = Groups.objects.get(user= self.user, group_name=self.group_name)
                raise ValidationError('This group already exists')
            except Groups.DoesNotExist:
                pass
            super(Groups, self).save(*args, **kwargs)