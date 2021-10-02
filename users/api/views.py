from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from users.models import Profile

from .serializers import (RegisterUserSerializer,
 UserSerializer,
 ProfileSerializer)

from rest_framework.authtoken.models import Token
from users.views import register_backend 
import requests

@api_view(['POST'])
def registration(request):
    if request.method == 'POST':
        serializer = RegisterUserSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data ['response'] = 'succefully registered a new user'
            data ['email'] = user.email
            data ['username'] = user.username
            # token = Token.objects.get(user=user).key
            # data ['token'] = token
        else:
            data = serializer.errors
        return Response(data)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_view(request):
    try:
        user = request.user
        profile = Profile.objects.get(user= user)
    except: 
        return Response(status= status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UserSerializer(user)
        myDict = serializer.data
        myDict['profile']=(user.profile.image.url)
        return Response( myDict)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def user_update(request):
    try:
        user = request.user
        profile = Profile.objects.get(user= user)
    except: 
        return Response(status= status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        user_serializer = UserSerializer(user, data = request.data)
        profile_serializer = ProfileSerializer(profile, data=request.data)
        data = {}
        if user_serializer.is_valid() and profile_serializer.is_valid():
            user_serializer.save()
            #! for backend based update the user in the backend
            data = user_serializer.data
            data['id'] = request.user.id
            print(data," my data")
            response = requests.put('http://127.0.0.1:8001/api/users/user-update', data = data, headers={ 'Authorization': 'Token e9e3d12642ed1b16a093d24951ed9efed1de413c'})

            profile_serializer.save()
            data['response'] = 'User infomation updated succefully'
            return Response( data=data)
        return Response(status= status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def registration(request):

# department - post per department 
# Hr - admin, supervisor ( different access permissions)