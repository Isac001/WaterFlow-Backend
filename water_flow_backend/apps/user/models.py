# Import models from Django's database module
from django.db import models
# Import gettext_lazy for internationalization of messages
from django.utils.translation import gettext_lazy as _
# Import base user classes and permission-related models from Django's auth module
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
# Import the custom UserManager from the user app's managers
from apps.user.managers import UserManager


# Define a custom User model inheriting from AbstractBaseUser and PermissionsMixin
class User(AbstractBaseUser, PermissionsMixin):

    # Define a character field for the user's name
    user_name = models.CharField(_("Name of User"), max_length=255, null=False)
    # Define an email field for the user's email, ensuring it's unique
    user_email = models.EmailField(_("Email of User"), max_length=255, null=False, unique=True)
    # Define a character field for the user's CPF (Brazilian individual taxpayer registry ID), ensuring it's unique
    user_cpf = models.CharField(_("CPF User"), max_length=14, null=False, unique=True)
    # Define a character field for the user's password
    password = models.CharField(_("Password of User"), max_length=255, null=False)

    # Define a boolean field to indicate if the user is an admin/staff
    is_staff = models.BooleanField(_("Admin?"), default=False)
    # Define a boolean field to indicate if the user account is active
    is_active = models.BooleanField(_("Active?"), default=True)
    # Define a boolean field to indicate if the user is trusty (custom flag)
    is_trusty = models.BooleanField(_("Trusty?"), default=True)

    # Specify the field to be used as the unique identifier for authentication
    USERNAME_FIELD = 'user_email'
    # Specify additional fields required when creating a user via createsuperuser
    REQUIRED_FIELDS = ['user_cpf']

    # Assign the custom UserManager to the objects manager for this model
    objects = UserManager()

    # Define the string representation of the model instance
    def __str__(self):

        # Return the user's email as their string representation
        return self.user_email
    
    # Define metadata for the model
    class Meta:

        # Specify the database table name for this model
        db_table = 'user'
        # Specify the application label for this model
        app_label = 'user'
        # Define database constraints for the model
        constraints = [
            # Ensure user_email values are unique across the table
            models.UniqueConstraint(fields=['user_email'], name='unique_user_email'),
            # Ensure user_cpf values are unique across the table
            models.UniqueConstraint(fields=['user_cpf'], name='unique_user_cpf'),
        ]