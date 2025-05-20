from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from apps.user.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    # User Fields
    user_name = models.CharField(_("Name of User"), max_length=255, null=False)
    user_email = models.EmailField(_("Email of User"), max_length=255, null=False, unique=True)
    user_cpf = models.CharField(_("CPF User"), max_length=14, null=False, unique=True)
    password = models.CharField(_("Password of User"), max_length=255, null=False)

    # Access and permission data
    is_staff = models.BooleanField(_("Admin?"), default=False)
    is_active = models.BooleanField(_("Active?"), default=True)
    is_trusty = models.BooleanField(_("Trusty?"), default=True)

    USERNAME_FIELD = 'user_email'
    REQUIRED_FIELDS = ['user_cpf']

    objects = UserManager()

    def __str__(self):

        return self.user_email
    
    class Meta:

        db_table = 'user'
        app_label = 'user'
        constraints = [
            models.UniqueConstraint(fields=['user_email'], name='unique_user_email'),
            models.UniqueConstraint(fields=['user_cpf'], name='unique_user_cpf'),
        ]

