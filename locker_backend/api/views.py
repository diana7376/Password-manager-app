from .models import PasswordItem
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PasswordItemSerializer


@api_view(['GET', 'POST'])
def get_post_password_items(request):
    if request.method == 'GET':
        data = get_password_items(request)
        return Response(data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        data = post_password_items(request)
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'PUT', 'DELETE'])
def get_put_delete_password_items(request, pk):
    if request.method == 'GET':
        data = get_specific_password_items(request, pk)
        return Response(data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        data = put_password_items(request, pk)
        return Response(data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        delete_password_items(request, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

def get_password_items(request):
    password_items = PasswordItem.objects.all()
    serializer = PasswordItemSerializer(password_items, many=True)
    return serializer.data

def post_password_items(request):
    serializer = PasswordItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_specific_password_items(request, pk):
    try:
        user = PasswordItem.objects.get(pk=pk)
    except PasswordItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PasswordItemSerializer(user)
    return serializer.data

def put_password_items(request, pk):
    try:
        user = PasswordItem.objects.get(pk=pk)
    except PasswordItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PasswordItemSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def delete_password_items(request, pk):
    try:
        user = PasswordItem.objects.get(pk=pk)
    except PasswordItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user.delete()
