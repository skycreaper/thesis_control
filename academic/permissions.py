from rolepermissions.permissions import register_object_checker
from mystie.roles import *

@register_object_checker()
def add_student(role, user, is_admin):
    if role == Admin:
        return True

    if user.is_admin == is_admin:
        return True
    
    return False

def list_student(role, user, is_admin):
    if role == Admin:
        return True

    if user.is_admin == is_admin:
        return True
    
    return False