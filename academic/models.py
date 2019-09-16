from users.models import CustomUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from rolepermissions.roles import assign_role

class CivilState(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Gender(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Nationality(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    origin_country = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class HealthInformation(models.Model):
    grupo_sanguineo = models.CharField(max_length=3)
    rh = models.CharField(max_length=1)
    eps = models.CharField(max_length=30)

class Rol(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class PersonalInformation(models.Model):
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    civil_state = models.ForeignKey(CivilState, on_delete=models.CASCADE)
    nationality = models.ForeignKey(Nationality, on_delete=models.CASCADE)
    # address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)
    health_information = models.OneToOneField(HealthInformation, on_delete=models.CASCADE)

class InstitutionalInformation(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    cvlac = models.CharField(max_length=200)
    institutional_email = models.EmailField('institutional email', null=False, blank=False, unique=True, default="default_email@unal.edu.co")

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique=True, primary_key=True)
    personal_information = models.OneToOneField(PersonalInformation, null=False, on_delete=models.CASCADE, default=-1)
    institutional_information = models.ForeignKey(InstitutionalInformation, null=False, on_delete=models.CASCADE, default=-1)
    objects=models.Manager()

# @receiver(post_save, sender=CustomUser)
# def student_for_new_user(sender, instance , created, **kwargs):
#     if created:
#         Student.objects.create(user=instance).save()

#udate

#delete

# Teacher model
class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique=True, primary_key=True)
    personal_information = models.OneToOneField(PersonalInformation, null=False, on_delete=models.CASCADE, default=-1)
    institutional_information = models.ForeignKey(InstitutionalInformation, null=False, on_delete=models.CASCADE, default=-1)
    objects=models.Manager()
    # user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, unique=True)
    # cvlacTeacher = models.CharField(max_length=200) # campo de prueba
    # objects=models.Manager()

# @receiver(post_save, sender=CustomUser)
# def teacher_for_new_user(sender, instance , created, **kwargs):
#     if created:
#         Teacher.objects.create(user=instance).save()


class Thesis(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1024*2)
    period = models.CharField(max_length=200)             # periodo
    # relacion con usuario director
    direct = models.CharField(max_length=200)
    student = models.CharField(max_length=200)            # id estuddiante
    porcentage = models.CharField(max_length=2)           # calculado auto
    state = models.CharField(max_length=2)                # para workflow
    create_date = models.DateTimeField('date published')


class Advance(models.Model):
    thesis = models.ForeignKey(Thesis, on_delete=models.CASCADE)
    description = models.TextField(max_length=1024*2)
    observation = models.TextField(max_length=1024*2)
    porcentage_proposed = models.CharField(max_length=200)
    porcentage_execute = models.CharField(max_length=200)
    state = models.CharField(max_length=2)                   # para workflow
    create_date = models.DateTimeField('date published')
