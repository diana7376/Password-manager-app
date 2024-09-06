from django.db import models
from django.db.models import ForeignKey



class Groups(models.Model):
    groupId = models.AutoField(primary_key=True)
    groupName = models.CharField(max_length=100)

    class Meta:
        db_table = 'groups'

    def __str__(self):
        return self.groupName


# Create your models here.
class PasswordItems(models.Model):
    itemName = models.CharField(max_length=100)
    userName = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    groupId = models.ForeignKey(Groups, db_column='groupId', on_delete=models.CASCADE)

    class Meta:
        db_table = 'password-items'

    def __str__(self):
        return self.itemName
