from django.shortcuts import render
from models import PasswordItem
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def get_password_items(request):
    pass

@api_view(['POST'])
def create_password_item(request):
    pass

@api_view(['GET', 'PUT', 'DELETE'])
def password_item_details(request, pk):
    pass
# Create your views here.
