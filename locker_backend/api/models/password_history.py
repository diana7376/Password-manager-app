from django.db import models
  # Adjust the import according to your project structure

class PasswordHistory(models.Model):
    from .password_items import PasswordItems
    pass_id = models.ForeignKey(PasswordItems, on_delete=models.CASCADE, db_column='pass_id')
    old_passwords = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'password-history'

    def __str__(self):
        return str(self.pass_id)
