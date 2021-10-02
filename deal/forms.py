from django import forms
from .models import Deal
from django.core.exceptions import ValidationError
from django.contrib import messages
import requests
from django.conf import settings

# deal creation form 
class DealCreationForm(forms.ModelForm):

    class Meta:
        # save to the user model ( dB)
        model = Deal
        # what form fields to use and in what order
        fields = [
            'title',
            'handler',
            'price',
            'status',
            'currency',
            ]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['date_created'].widget.attrs.update({'type':'date'})
    #     self.fields['date_created'].widget.attrs.update({'type':'textarea'})

    def clean(self):
        cleaned_data= super().clean()
        
        print(cleaned_data)




#  update user profile 
class DealUpdateForm(forms.ModelForm):

    class Meta:
        # save to the user model ( dB)
        model = Deal
        # what form fields to use and in what order
        fields =[
             'title',
            'status',
            'price',
            'currency',
        ]
    def clean(self):
        cleaned_data= super().clean()
        print('entered cleaning - updating ')
        # ! here we should send the data toward the API
        print(cleaned_data)

# #  update user profile 
# class DealUpdateForm2(forms.ModelForm):

#     class Meta:
#         # save to the user model ( dB)
#         model = Deal
#         # what form fields to use and in what order
#         fields =[
#             'title',
#             'status',
#             'price',
#             'currency',
#         ]
#     def clean(self):
#         cleaned_data= super().clean()
#         print('entered cleaning - updating ')
#         # ! here we should send the data toward the API
#         print(cleaned_data)

