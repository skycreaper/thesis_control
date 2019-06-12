from django.db import models
from django.contrib.auth.models import AbstractUser


# class User(AbstractUser):
#     is_student = models.BooleanField(default=False)
#     is_teacher = models.BooleanField(default=False)


class Student(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    host_field = models.CharField(max_length=500)   


class Teacher(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    guest_field = models.BooleanField(null=False)


class Thesis(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1024*2)
    period = models.CharField(max_length=200)             # periodo
    direct = models.CharField(max_length=200)             # relacion con usuario director
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