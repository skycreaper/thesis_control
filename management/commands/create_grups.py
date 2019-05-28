from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from academic.models import Thesis, Choice

# Grupo
new_group, created = Group.objects.get_or_create(name='student')
# Models
thesis = ContentType.objects.get_for_model(Thesis)
choice = ContentType.objects.get_for_model(Choice)

# Agregar Permiso a Grupo
# Thesis => academic.add_thesis + academic.chage_thesis + academic.view_thesis + academic.delete_thesis
thesis_add = Permission.objects.create(codename='can_add_thesis',
                                   name='Can add thesis',
                                   content_type=thesis)
thesis_change = Permission.objects.create(codename='can_change_thesis',
                                   name='Can change thesis',
                                   content_type=thesis)
thesis_view = Permission.objects.create(codename='can_view_thesis',
                                   name='Can view thesis',
                                   content_type=thesis)
new_group.permissions.add(thesis_add)
new_group.permissions.add(thesis_change)
new_group.permissions.add(thesis_view)