from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import PasswordItems, Groups, BaseUser, PasswordHistory


class PasswordItemSerializer(serializers.ModelSerializer):
    parent_lookup_kwargs = {
        'groups_pk' : 'groups_pk',
    }
    #userId = serializers.IntegerField(required=False,allow_null=True)
    class Meta:
        model = PasswordItems
        fields = '__all__'
        read_only_fields = ['user_id']  # Ensure userId is read-only

    def create(self, validated_data):
        # Assign the userId explicitly from the view
        validated_data['user_id'] = self.context['request'].user
        return super().create(validated_data)



class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = '__all__'
        read_only_fields = ['user_id']

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
        fields = ('user_name', 'email', 'password', 'password2',)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = BaseUser.objects.create(
            user_name=validated_data['user_name'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class PasswordHistorySerializer(serializers.ModelSerializer):
    updated_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")

    class Meta:
        model = PasswordHistory
        fields = '__all__'
