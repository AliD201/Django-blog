from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth.models import User
from .serializers import RegisterUserSerializer

from rest_framework.authtoken.models import Token



@api_view(['POST'])
def registration(request):
    if request.method == 'POST':
        serializer = RegisterUserSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data ['response'] = 'succefulklly registered a new user'
            data ['email'] = user.email
            data ['username'] = user.username
            token = Token.objects.get(user=user).key
            data ['token'] = token
        else:
            data = serializer.errors
        return Response(data)

