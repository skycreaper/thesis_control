from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    # fiels module
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    movile = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    birth_date = models.DateField(null=True, blank=True)
    cvlac = models.CharField(max_length=200)
    # fiels module

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email





