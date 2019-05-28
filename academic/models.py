from django.db import models


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