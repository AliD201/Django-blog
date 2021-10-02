from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

from django.contrib.auth.forms import PasswordResetForm

import requests
from django.core.exceptions import ValidationError
# registration form 
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        # save to the user model ( dB)
        model = User
        # what form fields to use and in what order
        fields =[
            'username',
            'email',
            'password1',
            'password2',
        ]
    def clean(self):
        cleaned_data= super().clean()
        print('entered cleaning')
        try:
            myuser = User.objects.get(username=cleaned_data['username'])
            print(myuser.id)
            response = requests.get(f'http://127.0.0.1:8001/api/users/user-details/{myuser.id}/',  headers={ 'Authorization': 'Token e9e3d12642ed1b16a093d24951ed9efed1de413c'})
            try:
                if response.status_code == 404:
                    print('user deleteing')
                    myuser.delete()
                    print('user deleteing')
            except:
                pass
        except:
            # user isn't present in app database
            pass
        data = cleaned_data
        data['password'] = data.pop('password1')
        # data['password'] = make_password(data.pop('password1'))
        data['password2'] = data['password']
        print("MYDATA")
        response = requests.post('http://127.0.0.1:8001/api/users/register', data = cleaned_data, headers={ 'Authorization': 'Token e9e3d12642ed1b16a093d24951ed9efed1de413c'})
        try :
            response = response.json()
            print(" MY response ")
            print(response)
            if not response.__contains__('response'):
                print("in")
                raise ValidationError(response)
        except:
            raise ValidationError(response)
        print('cleaning', cleaned_data)



#  update user profile 
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        # save to the user model ( dB)
        model = User
        # what form fields to use and in what order
        fields =[
            'username',
            'email',
        ]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        # save to the profile model ( dB)
        model = Profile
        # what form fields to use and in what order
        fields =[
            'image',
        ]



class EmailValidationOnForgotPassword(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__exact=email, is_active=True).exists():
            msg = ("There is no user registered with the specified E-Mail address.")
            self.add_error('email', msg)
        return email    
    
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('blog-home')
        print('hi')
        return super().dispatch(*args, **kwargs)