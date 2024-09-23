from django.db import models
from rest_framework.exceptions import ValidationError
from .groups import Groups
from .base_user import BaseUser  # Adjust the import according to your project structure
# Adjust the import according to your project structure
from api.models.encryption import decrypt_password, encrypt_password


# Create this file for encryption functions

class PasswordItems(models.Model):
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="passwordItems")
    item_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    url = models.CharField(max_length=255, null=True)
    comment = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'password-items'

    def __str__(self):
        return self.item_name

    def save(self, *args, **kwargs):
        from .password_history import PasswordHistory
        if self.pk:
            old_password_item = PasswordItems.objects.get(pk=self.pk)
            decrypted_old_password = decrypt_password(old_password_item.password)

            if decrypted_old_password != self.password:
                old_passwords = PasswordHistory.objects.filter(pass_id=self).values_list('old_passwords', flat=True)
                for old_password in old_passwords:
                    if decrypt_password(old_password) == self.password:
                        raise ValidationError("The new password must be different from previous passwords.")

                PasswordHistory.objects.create(
                    pass_id=self,
                    old_passwords=old_password_item.password
                )

        self.password = encrypt_password(self.password)
        super(PasswordItems, self).save(*args, **kwargs)
