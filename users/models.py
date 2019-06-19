from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    movile = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    birth_date = models.DateField(null=True, blank=True)
    cvlac = models.CharField(max_length=200)

    def __str__(self):
        return self.email