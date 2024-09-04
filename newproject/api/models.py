from django.db import models

# Create your models here.

"""
class User(models.Model):
    age = models.IntegerField()
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
"""

class Passwords(models.Model):
    password_id = models.AutoField(primary_key=True)
    platform = models.CharField(max_length=50)
    website = models.CharField(max_length=50)
    username = models.CharField(max_length=32)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=32)


