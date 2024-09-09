from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



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


class BaseUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        return self.get(username=username)


class BaseUser(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = BaseUserManager()

    class Meta:
        db_table = 'base-users'

    def __str__(self):
        return self.username
