from .models import PasswordItem
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PasswordItemSerializer


@api_view(['GET'])
def get_password_items(request):
    password_items = PasswordItem.objects.all()
    serializer = PasswordItemSerializer(password_items, many=True)
    # print(serializer)
    return Response(serializer.data)

@api_view(['POST'])
def create_password_item(request):
    serializer = PasswordItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_password_item(request, pk):
    try:
        user = PasswordItem.objects.get(pk=pk)
    except PasswordItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PasswordItemSerializer(user)
    return Response(serializer.data)

@api_view(['PUT'])
def update_password_item(request, pk):
    try:
        user = PasswordItem.objects.get(pk=pk)
    except PasswordItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PasswordItemSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_password_item(request, pk):
    try:
        user = PasswordItem.objects.get(pk=pk)
    except PasswordItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
