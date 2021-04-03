from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

from django.conf import settings
from rest_framework.authtoken.models import Token

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


# this have been sepperated from the create profile function to clairfy what it is doing
# and imply some sepration between the two processes 
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     print('signal three recieved')
#     # when the user is created generate a token
#     if created:
#         Token.objects.create(user=instance)
