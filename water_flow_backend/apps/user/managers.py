from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):

    def create_user(self, user_email, password, **extra_fields):

        if not user_email:

            raise ValueError(_("The Email field must be set"))
        
        email = self.normalize_email(user_email)

        user = self.model(user_email=email, **extra_fields)

        user.set_password(password)

        user.save(using=self.db)

        return user
    
    def create_superuser(self, user_email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_trusty', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        
        return self.create_user(user_email, password, **extra_fields)