from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import PasswordItems, Groups, BaseUser, PasswordHistory

class GroupsSerializer(serializers.ModelSerializer):
    groupName = serializers.CharField(source= 'group_name')
    userId = serializers.PrimaryKeyRelatedField(source= 'user_id', queryset= BaseUser.objects.all(), required= False)
    groupId = serializers.PrimaryKeyRelatedField(source= 'group_id', queryset= Groups.objects.all(), required= False)
    class Meta:
        model = Groups
        fields = ['groupName', 'groupId', 'userId']

    def create(self, validated_data):
        # Assign the userId explicitly from the view
        validated_data['user_id'] = self.context['request'].user
        return super().create(validated_data)


class PasswordItemSerializer(serializers.ModelSerializer):
    parent_lookup_kwargs = {
        'groups_pk' : 'groups_pk',
    }

    itemName = serializers.CharField(source= 'item_name')
    userName= serializers.CharField(source= 'username')
    groupId = serializers.PrimaryKeyRelatedField(source='group_id', queryset=Groups.objects.all())
    userId = serializers.PrimaryKeyRelatedField(source= 'user_id', queryset= BaseUser.objects.all(), required= False)
    class Meta:
        model = PasswordItems
        fields = ['id', 'itemName', 'userName', 'password', 'url', 'comment', 'userId', 'groupId']

    def create(self, validated_data):
        # Assign the userId explicitly from the view
        validated_data['user_id'] = self.context['request'].user
        return super().create(validated_data)

class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
       model = BaseUser
       fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

        # token['username'] = user.username
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['access'] = str(refresh.access_token)
        data.pop('refresh', None)
        return data





class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=BaseUser.objects.all())]
    )

    class Meta:
        model = BaseUser
        fields = ('username', 'email', 'password', 'password2',)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = BaseUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class PasswordHistorySerializer(serializers.ModelSerializer):

    passId = serializers.PrimaryKeyRelatedField(source= 'pass_id', queryset= PasswordItems.objects.all())
    oldPasswords = serializers.CharField(source='old_passwords')
    updatedAt = serializers.DateTimeField(source='updated_at', format="%d-%m-%Y %H:%M:%S")
    class Meta:
        model = PasswordHistory
        fields = ['id', 'oldPasswords', 'updatedAt', 'passId']
