from rest_framework import serializers
from .models import PasswordItem

class PasswordItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordItem
        fields = '__all__'