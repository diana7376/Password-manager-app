from django.db import models
from .base_user import BaseUser  # Adjust the import according to your project structure

class Groups(models.Model):
    group_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="groups")
    group_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'groups'

    def __str__(self):
        return self.group_name
