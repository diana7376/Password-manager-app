from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from cryptography.fernet import Fernet
from rest_framework.exceptions import ValidationError

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
    user_id = models.AutoField(primary_key=True)
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
    group_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="groups")
    group_name = models.CharField(max_length=100)
    class Meta:
        db_table = 'groups'

    def __str__(self):
        return self.group_name


# Create your models here.
class PasswordItems(models.Model):
    group_id = models.ForeignKey(Groups, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="passwordItems")
    item_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    url = models.CharField(max_length=255, null=True)
    comment = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'password-items'

    def __str__(self):
        return self.item_name

    # Overriding save method to handle password history
    def save(self, *args, **kwargs):
        # Check if it's an update (the object already exists in the database)
        if self.pk:
            old_password_item = PasswordItems.objects.get(pk=self.pk)
            decrypted_old_password = decrypt_password(old_password_item.password)

            # Check if the decrypted password is being updated
            if decrypted_old_password != self.password:
                # Fetch old passwords from PasswordHistory
                old_passwords = PasswordHistory.objects.filter(pass_id=self).values_list('old_passwords', flat=True)
                for old_password in old_passwords:
                    if decrypt_password(old_password) == self.password:
                        raise ValidationError("The new password must be different from previous passwords.")

                # Create a new entry in PasswordHistory
                PasswordHistory.objects.create(
                    pass_id=self,
                    old_passwords=old_password_item.password
                )

        # Encrypt password before saving
        self.password = encrypt_password(self.password)

        # Call the original save method
        super(PasswordItems, self).save(*args, **kwargs)


class PasswordHistory(models.Model):
    pass_id = models.ForeignKey(PasswordItems, on_delete=models.CASCADE)
    old_passwords = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'password-history'

    def __str__(self):
        return self.pass_id

