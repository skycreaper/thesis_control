from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, default="default_username", unique=True)
    # email = models.EmailField(_('email address'), unique=True)
    # fiels module
    # is_student = models.BooleanField(default=False)
    # is_teacher = models.BooleanField(default=False)
    
    # cvlac = models.CharField(max_length=200)
    # fiels module

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [username]

    objects = CustomUserManager()

    def __str__(self):
        return self.username





