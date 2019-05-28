from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from academic.models import Thesis, Advance

# Grupo
new_group, created = Group.objects.get_or_create(name='student')
# Models
thesis = ContentType.objects.get_for_model(Thesis)
advance = ContentType.objects.get_for_model(Advance)

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
# Choice
advance_add = Permission.objects.create(codename='can_add_advance',
                                   name='Can add advance',
                                   content_type=advance)
advance_change = Permission.objects.create(codename='can_change_advance',
                                   name='Can change advance',
                                   content_type=advance)
advance_view = Permission.objects.create(codename='can_view_advance',
                                   name='Can view advance',
                                   content_type=advance)

new_group.permissions.add(thesis_add)
new_group.permissions.add(thesis_change)
new_group.permissions.add(thesis_view)

new_group.permissions.add(advance_add)
new_group.permissions.add(advance_change)
new_group.permissions.add(advance_view)
