from rolepermissions.roles import AbstractUserRole
from django.contrib.auth.models import User
from rolepermissions.permissions import available_perm_status

class Manager(AbstractUserRole):
    available_permissions = {
        'create_blog': True,
        'delete_blog': True,
        'edit_blog': True,
    }

class Writer(AbstractUserRole):
    available_permissions = {
        'create_blog': True,
        'delete_blog': False,
        'edit_blog': True,
    }

class Reader(AbstractUserRole):
    available_permissions = {
        'create_blog': False,
        'delete_blog': False,
        'edit_blog': False,
    }

import requests
def permissionCheck(username ,permission):
    try:
        response = requests.get('http://127.0.0.1:8001/api/users/permission', data = {"username":username, "permission": permission}, headers={ 'Authorization': 'Token e9e3d12642ed1b16a093d24951ed9efed1de413c'})  
        print("PERMISSION CHECK { "+ response.text + " }")
        if response.text == True or response.text == "true" :
            return True
        else:
            return False
    except:
        print("PERMISSION CHECK { Failed }")
        return False

def CanEdit(User):
    try:
        # permissions =available_perm_status(User)
        # if User.has_perm('auth.edit_blog'):
        if permissionCheck(User.username, 'auth.edit_blog'):
            return True
        else:
            return False
    except:
        return False
    
def canCreate(User):
    try:
        # permissions =available_perm_status(User)
        # print(User.get_all_permissions())
        # if User.has_perm('auth.create_blog'):
        if permissionCheck(User.username, 'auth.create_blog'):
            return True
        else:
            return False
    except:
        return False

def canDelete(User):
    try:
        # permissions =available_perm_status(User)
        # if User.has_perm('auth.delete_blog'):
        if permissionCheck(User.username, 'auth.delete_blog'):
            return True
        else:
            return False
    except:
        return False
    

