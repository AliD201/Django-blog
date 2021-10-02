from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

from django.conf import settings
from rest_framework.authtoken.models import Token

import requests

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    print('signal one recieved')
    # when the user is created create a profile object
    if created:
        Profile.objects.create(user=instance)

 
# this one is just to update the profile upon any user change
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    print('signal two recieved')
    instance.profile.save()

@receiver(pre_save, sender=User)
def detect_password_change(sender, instance, **kwargs):
    """
    Checks if the user changed his password
    """
    if instance._password is None:
        return

    try:
        user = User.objects.get(id=instance.id)
    except User.DoesNotExist:
        return

    print("password changed")
    # if you get here, the user changed his password
    data = {'id':user.id, 'password':instance._password }
    response = requests.put('http://127.0.0.1:8001/api/users/passwordReset', data = data, headers={ 'Authorization': 'Token e9e3d12642ed1b16a093d24951ed9efed1de413c'})
    print(response.content)
    


# this have been sepperated from the create profile function to clairfy what it is doing
# and imply some sepration between the two processes 
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     print('signal three recieved')
#     # when the user is created generate a token
#     if created:
#         Token.objects.create(user=instance)
