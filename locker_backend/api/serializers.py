from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import PasswordItems, Groups, BaseUser, PasswordHistory
from .models.invitation import Invitation


class GroupsSerializer(serializers.ModelSerializer):
    groupName = serializers.CharField(source= 'group_name')
    groupId = serializers.IntegerField(source= 'group_id', read_only=True)
    userId = serializers.PrimaryKeyRelatedField(source='user', read_only=True)

    class Meta:
        model = Groups
        fields = ['groupId', 'groupName', 'userId']
        read_only_fields = ['userId']

    def create(self, validated_data):
        # Assign the userId explicitly from the view
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class PasswordItemSerializer(serializers.ModelSerializer):
    parent_lookup_kwargs = {
        'groups_pk' : 'groups_pk',
    }

    itemName = serializers.CharField(source= 'item_name')
    userName= serializers.CharField(source= 'username')
    groupId = serializers.PrimaryKeyRelatedField(source= 'group', queryset=Groups.objects.all(), required=False)
    passId = serializers.IntegerField(source= 'id', read_only=True)
    userId = serializers.PrimaryKeyRelatedField(source='user', read_only=True)

    class Meta:
        model = PasswordItems
        fields = ['passId','itemName', 'userName', 'password', 'url', 'comment', 'groupId', 'userId']
        read_only_fields = ['userId']  # Ensure userId is read-only

    def validate(self, attrs):
        user = self.context['request'].user
        group = attrs.get('group')

        # Check if the group belongs to the user
        if group and group.user != user:
            raise serializers.ValidationError("You do not have permission to add or update this password item in this group.")

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        item_name = validated_data['item_name']

        if PasswordItems.objects.filter(user= user, item_name= item_name):
            raise serializers.ValidationError({'item_name' : 'A PasswordItem with this name already exists.'})

        validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'group' not in validated_data:
            validated_data['group'] = None

        validated_data['user'] = self.context['request'].user
        return super().update(instance, validated_data)



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

    oldPassword = serializers.CharField(source= 'old_passwords')
    updatedAt = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", source='updated_at')
    passId = serializers.PrimaryKeyRelatedField(source='pass_id', read_only=True)

    class Meta:
        model = PasswordHistory
        fields = ['id', 'oldPassword', 'updatedAt', 'passId']

class InvitationSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.group_name')

    class Meta:
        model = Invitation
        fields = ['id', 'group_name', 'created_at']