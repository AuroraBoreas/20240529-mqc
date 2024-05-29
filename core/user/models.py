import typing

from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, Group
from django.core.validators import EmailValidator


class AppUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields: typing.Any):
        if not email: raise ValueError('Email is required')
        if not password: raise ValueError('Password is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields: typing.Any):
        if not email: raise ValueError('Email is required')
        if not password: raise ValueError('Password is required')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class AppUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(validators=[EmailValidator(message='Enter a valid email address.')], max_length=50, unique=True)
    username = models.CharField(max_length=100, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    country = models.CharField(max_length=100)
    date_joined = models.DateField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = AppUserManager()
    groups = models.ManyToManyField(Group, blank=True)
    # class Meta:
    #     permissions = [
    #         ("can_add_custom_data", "Can add custom data"),
    #         ("can_change_custom_data", "Can change custom data"),
    #         ("can_delete_custom_data", "Can delete custom data"),
    #         ("can_view_custom_data", "Can view custom data"),
    #     ]
    def __str__(self) -> str:
        return self.username
    
    def get_full_name(self) -> str:
        return self.username

    def get_short_name(self) -> str:
        return self.username or self.email.split('@')[0]