from rest_framework import serializers
from .models import PasswordItem, Groups


class PasswordItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordItem
        fields = '__all__'

class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = '__all__'