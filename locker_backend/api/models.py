from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from cryptography.fernet import Fernet


ENCRYPTION_KEY = b'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='
cipher_suite = Fernet(ENCRYPTION_KEY)

def encrypt_password(password):
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(password):
    return cipher_suite.decrypt(password.encode()).decode()

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


class Groups(models.Model):
    groupId = models.AutoField(primary_key=True)
    userId = models.ForeignKey(BaseUser, db_column='userId', on_delete=models.CASCADE, related_name="groups")
    groupName = models.CharField(max_length=100)
    class Meta:
        db_table = 'groups'

    def __str__(self):
        return self.groupName


# Create your models here.
class PasswordItems(models.Model):
    groupId = models.ForeignKey(Groups, db_column='groupId', on_delete=models.CASCADE, null=True)
    userId = models.ForeignKey(BaseUser, db_column='userId', on_delete=models.CASCADE, related_name="passwordItems")
    itemName = models.CharField(max_length=100)
    userName = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    url = models.CharField(max_length=255, null=True)
    comment = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'password-items'

    def __str__(self):
        return self.itemName

    # Overriding save method to handle password history
    def save(self, *args, **kwargs):
        # Check if it's an update (the object already exists in the database)
        if self.pk:
            old_password_item = PasswordItems.objects.get(pk=self.pk)
            # Check if the password is being updated
            if old_password_item.password != self.password:
                # Create a new entry in PasswordHistory
                PasswordHistory.objects.create(
                    passId=self,
                    old_passwords=old_password_item.password
                )
        self.password = encrypt_password(self.password) #ENCRYPTION
        # Call the original save method
        super(PasswordItems, self).save(*args, **kwargs)


class PasswordHistory(models.Model):
    # userId = models.ForeignKey(BaseUser, db_column='userId', on_delete=models.CASCADE, null=True)
    passId = models.ForeignKey(PasswordItems, db_column='passId', on_delete=models.CASCADE)
    old_passwords = models.CharField(max_length=255)

    class Meta:
        db_table = 'password-history'

    def __str__(self):
        return self.passId

