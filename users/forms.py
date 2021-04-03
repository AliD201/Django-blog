from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

from django.contrib.auth.forms import PasswordResetForm

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
    # image = forms.ImageField(default ='default.jpg', upload_to='profile_pics')
    class Meta:
        # save to the user model ( dB)
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