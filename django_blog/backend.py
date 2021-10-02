# customers/backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

# from customers.models import Customer
import requests
from django.core import serializers
from django.contrib.auth.models import Permission
import re


class UserBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        username = kwargs['username']
        password = kwargs['password']

        # try:
        response = requests.post('http://127.0.0.1:8001/api/users/login', data = {"username":username, "password": password}, headers={ 'Authorization': 'Token e9e3d12642ed1b16a093d24951ed9efed1de413c'})
 
        try :
            response = response.json()
            print("11111", response)
            print("-------------------")
        except:
            return None
        # print(response)
        # print(response[0])
        userArr = []
        user = response[0]
        groups = response[1]
        permissions = response[2]
        i = 0;
        for element in response :
            # try:
            if i == 2:
                break
            Emptygenerator = True
            deserialized = serializers.deserialize("json", element)
            print((deserialized), '======================----------')
            for obj in deserialized:
                Emptygenerator = False
                print(i, "-----------------")
                print(obj.object)
                print(type(obj.object))
                userArr.append(obj.object)
            if Emptygenerator:
                userArr.append([])
            # except Exception:
            #     print("error")
            #     print(Exception)
            i += 1
            # print(type(obj))
            # print((obj.object.email))
            # print(obj.fields.email)
            # if i == 0:
            #     element.object.save()
            # print(element.object)
            # userArr.append(obj.boject)
        userArr.append(permissions)
        print('==========')
        print(userArr)
        
        # print(userArr[0].get_all_permissions())
        try:
            userArr[0].groups.add(userArr[1])
        except Exception:
            print("empty group")
        # for permission in userArr[2]:
        #     myperm= re.sub('^[a-zA-Z].*\.', '', permission)
        #     permission =  Permission.objects.get(codename=myperm)
        #     userArr[0].user_permissions.add(permission)
        # userArr[0].user_permissions.set(userArr[2])
        userArr[0].save()
        user = User.objects.get(id=userArr[0].id)
        # print(user.object)
        if(not user.is_superuser):
            user.user_permissions.clear()
            for permission in userArr[2]:
                myperm= re.sub('^[a-zA-Z].*\.', '', permission)
                permission =  Permission.objects.get(codename=myperm)
                user.user_permissions.add(permission)


        
        # user.save()
        return userArr[0]
        # print("end")
 
    # def get_user(self, user_id):
    #     try:
    #         response = requests.get(f'http://127.0.0.1:8001/api/users/user-details/{user_id}/')
    #         response = response.json()
    #         print(response)
    #         print("got him")
    #         for obj in serializers.deserialize("json", response):
    #             print(obj.object.groups.all())
    #             print(obj.object.get_all_permissions())
    #             return obj.object
    #     except :
    #         return None