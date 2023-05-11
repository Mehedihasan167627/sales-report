from django.db import models 
from .managers import UserManager
from django.contrib.auth.models import (
    AbstractBaseUser
)
from django.utils.html import format_html


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    ) 
    full_name=models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin 


