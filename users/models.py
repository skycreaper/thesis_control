from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
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