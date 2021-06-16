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

def CanEdit(User):
    try:
        # permissions =available_perm_status(User)
        if User.has_perm('auth.edit_blog'):
            return True
        else:
            return False
    except:
        return False
    
def canCreate(User):
    try:
        # permissions =available_perm_status(User)
        # print(User.get_all_permissions())
        if User.has_perm('auth.create_blog'):
            return True
        else:
            return False
    except:
        return False

def canDelete(User):
    try:
        # permissions =available_perm_status(User)
        if User.has_perm('auth.delete_blog'):
            return True
        else:
            return False
    except:
        return False
    

