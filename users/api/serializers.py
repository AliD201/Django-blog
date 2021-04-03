from rest_framework import serializers
from blog.models import Post
from django.contrib.auth.models import User

from users.models import Profile

class RegisterUserSerializer(serializers.ModelSerializer):

    # write only will make the the serilizer ignore this field upon serialization
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            # to cover the passwrod and store it is hash only 
            'password': {'write_only': True}
        }
    
    def save(self, *args, **kwargs):
        user = User(email= self.validated_data['email'],
        username = self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'passwrods not matching'})
        # JASON : {'password': 'passwrods not matching'}  # from raise
    
        user.set_password(password)
        user.save(args, kwargs)
        return user


class UserSerializer ( serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'username']
        # fields = ['pk', 'email', 'username']


class ProfileSerializer ( serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['image']