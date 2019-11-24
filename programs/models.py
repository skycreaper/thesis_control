from django.db import models

# Create your models here.
class Program(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, null=True, blank=True)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)

class SubProgram(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)

class ProgramTask(models.Model):
    name = models.CharField(max_length=200)
    comentary = models.CharField(max_length=500, null=True, blank=True)
    sub_program = models.ForeignKey(SubProgram, on_delete=models.CASCADE)
    acumulate_percentage = 0

class TaskAdvance(models.Model):
    comentary = models.TextField(max_length=1024*2)
    task_file = models.FileField("file", upload_to="task_documents", max_length=100)
    percentage = models.IntegerField()