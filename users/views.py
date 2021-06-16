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



@login_required
def profile(request):
    if (request.method ==  'POST'):
        user_form = UserUpdateForm(request.POST,  instance = request.user)
        # additional data is the file data
        profile_form = ProfileUpdateForm(request.POST, request.FILES,
        instance = request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
          
            profile_form.save()

            messages.success(request,f'account information updated succefully')
           
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


class MyPasswordResetView(auth_views.PasswordResetView):

    def dispatch(self, *args, **kwargs):
        
        return super().dispatch(*args, **kwargs)


class MyPasswordResetDoneView(auth_views.PasswordResetDoneView):

    def dispatch(self, *args, **kwargs):
        
        return super().dispatch(*args, **kwargs)

class MyPasswordResetCompleteView(auth_views.PasswordResetCompleteView):

    def dispatch(self, *args, **kwargs):
     
        return super().dispatch(*args, **kwargs)



class MyPasswordResetConfirmView(auth_views.PasswordResetConfirmView):

    def dispatch(self, *args, **kwargs):
        
        return super().dispatch(*args, **kwargs)