from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
import re
# from django.db import models

# Create your views here.

def register(request):
    if (request.method ==  'POST'):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save() # store the user 
            username = form.cleaned_data.get('username')
            # user = User.objects.get(username=username)
            # print( user.get_all_permissions() , " new user permissiosn")
            messages.success(request,f'  {username}  account created succefully')
            return redirect('login')
    else:
        if request.user.is_authenticated:
            return redirect('/')
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form} )

import requests 
from django.contrib.auth.hashers import make_password
from django import forms
def register_backend(request):
    if (request.method ==  'POST'):
        form = UserRegisterForm(request.POST)
        # response = requests.post(f'http://127.0.0.1:8001/api/users/user-details/<int:id>/', data = form.cleaned_data, headers={ 'Authorization': 'Token e9e3d12642ed1b16a093d24951ed9efed1de413c'})
        if form.is_valid():
            print(form.cleaned_data)
            print("in99")
            # data = form.cleaned_data
            # data['password'] = data.pop('password1')
            # # data['password'] = make_password(data.pop('password1'))
            # data['password2'] = data['password']
            
            # response = requests.post('http://127.0.0.1:8001/api/users/register', data = form.cleaned_data, headers={ 'Authorization': 'Token e9e3d12642ed1b16a093d24951ed9efed1de413c'})
            # try :
            #     response = response.json()
            #     print(" MY response ")
            #     print(response)
            #     if not response.__contains__('response'):
            #         print("in")
            #         for key in response.keys():
            #             # raise form.ValidationError(response[key][0])
            #             messages.warning(request, f'{ key } : {response[key][0]}')
            #         return render(request, 'users/register.html', {'form': form} )

            # except:
            #     # raise ValidationError(response)
            #     for key in response.keys():
            #         messages.warning(request, f'{ key }  {response[key]}')
            #     return redirect('register')
         
            # form.save() # store the user 
            username = form.cleaned_data.get('username')
            messages.success(request,f'  {username}  account created succefully')
            return redirect('login')
    else:
        if request.user.is_authenticated:
            return redirect('/')
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form} )

@login_required
def profile(request):
    if (request.method ==  'POST'):
        user_form = UserUpdateForm(request.POST,  instance = request.user)
        # additional data is the file data
        profile_form = ProfileUpdateForm(request.POST, request.FILES,
        instance = request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            #! for backend based update the user in the backend
            data = user_form.cleaned_data
            data['id'] = request.user.id
            print(data," my data")
            response = requests.put('http://127.0.0.1:8001/api/users/user-update', data = data, headers={ 'Authorization': 'Token e9e3d12642ed1b16a093d24951ed9efed1de413c'})
            
            profile_form.save()
            print(response)
            print(response.content)

            # if response["response"]:
            messages.success(request,f'account information updated succefully')
            # else:
            #     messages.warning(request, f'unable to update user due {response}')
            # this redirect is to prevent the re-submitting message from the browser
            return redirect('profile')
           
    else:
        user_form = UserUpdateForm(instance = request.user)
        profile_form = ProfileUpdateForm(instance = request.user.profile)


    permissions = request.user.get_all_permissions()
    permissionsArr = []
    for i in permissions:
        permissionsArr.append(i)

    print(permissionsArr)
    i = 0
    while i < len(permissionsArr):
        permissionsArr[i] = re.sub('^[a-zA-Z].*\.', '', permissionsArr[i])
        permissionsArr[i] = permissionsArr[i].replace("_", ' ').capitalize()
        i+= 1
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'permissions': permissionsArr
        } 
    return render(request, 'users/profile.html',context)

from django.core import serializers
class MyPasswordResetView(auth_views.PasswordResetView):

    def dispatch(self, *args, **kwargs):
        print('First view')
        
        if self.request.method == "POST":   
            print(self.request.POST['email'])
            my_email = self.request.POST['email']
            response = requests.get(f'http://127.0.0.1:8001/api/users/user-details/{my_email}', headers={ 'Authorization': 'Token e9e3d12642ed1b16a093d24951ed9efed1de413c'})
            try:
                response = response.json()
                print(response)
                deserialized = serializers.deserialize("json", response)
                for obj in deserialized:
                    user= obj.object
                user.save()
                print((user))
            except:
                print("issue")
                pass
        return super().dispatch(*args, **kwargs)


class MyPasswordResetDoneView(auth_views.PasswordResetDoneView):

    def dispatch(self, *args, **kwargs):
        print('Second view')
        return super().dispatch(*args, **kwargs)

class MyPasswordResetCompleteView(auth_views.PasswordResetCompleteView):

    def dispatch(self, *args, **kwargs):
        print(*args)
        print('Third view')
        return super().dispatch(*args, **kwargs)



class MyPasswordResetConfirmView(auth_views.PasswordResetConfirmView):

    def dispatch(self, *args, **kwargs):
        print('Fourth view')
        # if self.request.method == "POST":   
        #     print(self.request.POST)
        #     print(self.request.user )
        #     if self.request.POST['new_password1'] == self.request.POST['new_password2']:
        #         print('send to the backend')
        #         # response = requests.put('http://127.0.0.1:8001/api/users/user-update', data = data, headers={ 'Authorization': 'Token e9e3d12642ed1b16a093d24951ed9efed1de413c'})

        
        return super().dispatch(*args, **kwargs)