from rolepermissions.roles import AbstractUserRole


class Admin(AbstractUserRole):
    available_permissions = {
        'add_student': True,
        'edit_student': True,
        'remove_student': True,
    }

class Student(AbstractUserRole):
    available_permissions = {
        'add_avance': True,
    }

class Teacher(AbstractUserRole):
    available_permissions = {
        'list_student': True,
        'detail_student': True,
        'add_tesis': True
    }