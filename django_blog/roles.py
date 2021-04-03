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
        'edit_blog': False,
    }

class Reader(AbstractUserRole):
    available_permissions = {
        'create_blog': False,
        'delete_blog': False,
        'edit_blog': False,
    }

def CanEdit(User):
    try:
        permissions = available_perm_status(User)
        if permissions['edit_blog']:
            return True
        else:
            return False
    except:
        return False
    
def canCreate(User):
    try:
        permissions = available_perm_status(User)
        if permissions['create_blog']:
            return True
        else:
            return False
    except:
        return False
    

