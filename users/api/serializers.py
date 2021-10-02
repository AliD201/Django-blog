from rest_framework import serializers
from blog.models import Post
from django.contrib.auth.models import User

from users.models import Profile
import requests 
from django.core import serializers as serializers2

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
    def to_internal_value(self, data):
        print("validatin")
        print(data)
        try:
            myuser = User.objects.get(username=data['username'])
            print(myuser.id)
            response = requests.get(f'http://127.0.0.1:8001/api/users/user-details/{myuser.id}/',  headers={ 'Authorization': 'Token e9e3d12642ed1b16a093d24951ed9efed1de413c'})
            response = (response.json())
            print(response)
            deserialized = (serializers2.deserialize("json", response))
            try:
                # check if user is deleted from the IAM and make sure it is deleted here
                if response.status_code == 404:
                    print('user deleteing')
                    myuser.delete()
                    print('user deleteing')
            except:
                pass
            username = ''
            for obj in deserialized:
                if(obj.object.username != data['username']):
                    myuser.delete()
        except:
            # user isn't present in app database
            pass
        return super().to_internal_value(data)

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
        # ! back end
        
       
        print("MYDATA")
        response = requests.post('http://127.0.0.1:8001/api/users/register', data = self.validated_data, headers={ 'Authorization': 'Token e9e3d12642ed1b16a093d24951ed9efed1de413c'})
        try :
            response = response.json()
            print(" MY response ")
            print(response)
            if not response.__contains__('response'):
                print("in")
                raise ValidationError(response)
        except:
            raise ValidationError(response)
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