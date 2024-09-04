from http.client import responses
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import  status
from .models import Passwords
from .serializer import PasswordSerializer

@api_view(['GET'])
def get_passwords(request):
    passwords = Passwords.objects.all().values()
    return Response(passwords)

@api_view(['POST'])
def create_password(request):
    data = request.data

    required_fields = ["platform", "website", "email", "password", "username"]
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return Response({"error" : f"Missing required fields: {', '.join(missing_fields)}"},status=status.HTTP_400_BAD_REQUEST)

    passwords = Passwords(
        platform=data["platform"],
        website=data['website'],
        email=data['email'],
        username=data['username'],
        password=data['password']
    )
    passwords.save()

    response_data = {
        "id" : passwords.password_id,
        "platform" : passwords.platform,
        "website" : passwords.website,
        "email" : passwords.email,
        "username" : passwords.username,
        "password" : passwords.password
    }

    return Response(response_data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def password_details(request, pk):
    try:
        password = Passwords.objects.get(pk=pk)
    except Passwords.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # serializer = PasswordSerializer(password)

        response_data = {
            "id": password.password_id,
            "platform": password.platform,
            "website": password.website,
            "email": password.email,
            "username": password.username,
            "password": password.password
        }

        # return Response(serializer.data)
        return Response(response_data, status=status.HTTP_200_OK)


    elif request.method == 'PUT':
        data = request.data

        required_fields = ["platform", "website", "email", "password", "username"]
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return Response({"error": f"Missing required fields: {', '.join(missing_fields)}"},
                            status=status.HTTP_400_BAD_REQUEST)

        password.platform=data['platform']
        password.website=data['website']
        password.email=data['email']
        password.username=data['username']
        password.password=data['password']

        password.save()

        response_data = {
            "id": password.password_id,
            "platform": password.platform,
            "website": password.website,
            "email": password.email,
            "username": password.username,
            "password": password.password
        }

        return Response(response_data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        password.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




"""
from .models import User
from .serializer import UserSerializer

# Create your views here.

@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_passwords(request):
    password_li = ["1234567890", "iashviafhpaohih", "ZXCVBNM", "password", "0987654321"]
    return Response(password_li)

@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""

def check(request):
    return HttpResponse('Works')