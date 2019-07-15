from users.models import CustomUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    cvlacStudent = models.CharField(max_length=200) # campo de prueba
    objects=models.Manager()

@receiver(post_save, sender=CustomUser)
def student_for_new_user(sender, instance , created, **kwargs):
    if created:
        Student.objects.create(user=instance).save()

#udate

#delete

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    cvlacTeacher = models.CharField(max_length=200) # campo de prueba
    objects=models.Manager()

@receiver(post_save, sender=CustomUser)
def teacher_for_new_user(sender, instance , created, **kwargs):
    if created:
        Teacher.objects.create(user=instance).save()


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
