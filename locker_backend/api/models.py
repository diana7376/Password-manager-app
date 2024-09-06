from django.db import models
from django.db.models import ForeignKey


# Create your models here.
class PasswordItem(models.Model):
    itemName = models.CharField(max_length=100)
    userName = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = 'password-items'

    def __str__(self):
        return self.itemName

class Groups(models.Model):
    groupId = models.AutoField(primary_key=True)
    itemId = models.ForeignKey(PasswordItem, on_delete=models.CASCADE)
    groupName = models.CharField(max_length=100)

    class Meta:
        db_table = 'groups'

    def __str__(self):
        return self.groupName