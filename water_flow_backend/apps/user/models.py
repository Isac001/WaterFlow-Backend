# Django imports
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Project imports
from apps.user.managers import UserManager


# Custom User model
class User(AbstractBaseUser, PermissionsMixin):

    """
    Custom user model that uses email for authentication instead of username.
    """

    # User fields
    user_name = models.CharField(_("Name of User"), max_length=255)
    user_email = models.EmailField(_("Email of User"), max_length=255, unique=True)
    user_cpf = models.CharField(_("CPF User"), max_length=14, unique=True)
    password = models.CharField(_("Password of User"), max_length=255)

    # Boolean flags for user status and permissions
    is_staff = models.BooleanField(
        _("Admin status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    # Boolean flags for user status and permissions
    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    # Boolean flags for user status and permissions
    is_trusty = models.BooleanField(
        _("Trusty status"),
        default=True,
        help_text=_("Designates whether this user is considered trustworthy."),
    )

    # Manager and authentication fields
    objects = UserManager()
    USERNAME_FIELD = 'user_email'
    REQUIRED_FIELDS = ['user_name', 'user_cpf']

    # String representation of the model
    def __str__(self):
        """Returns the email of the user as its string representation."""
        return self.user_email
    
    # Meta class for model settings
    class Meta:

        """
        Model metadata configuration.
        """
        app_label = 'user'
        db_table = 'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        constraints = [
            models.UniqueConstraint(fields=['user_email'], name='unique_user_email'),
            models.UniqueConstraint(fields=['user_cpf'], name='unique_user_cpf'),
        ]