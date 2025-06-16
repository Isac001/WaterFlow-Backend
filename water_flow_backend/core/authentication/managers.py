# Import BaseUserManager for creating custom user managers
from django.contrib.auth.models import BaseUserManager
# Import gettext_lazy for internationalization of messages
from django.utils.translation import gettext_lazy as _

# Define a custom user manager class inheriting from BaseUserManager
class UserManager(BaseUserManager):

    # Define a method to create a regular user
    def create_user(self, user_email, password, **extra_fields):

        # Check if the user_email field is provided
        if not user_email:

            # Raise a ValueError if email is not provided
            raise ValueError(_("The Email field must be set"))
        
        # Normalize the email address (e.g., lowercase the domain part)
        email = self.normalize_email(user_email)

        # Create a new user instance with the normalized email and other fields
        user = self.model(user_email=email, **extra_fields)

        # Set the user's password securely (hashes the password)
        user.set_password(password)

        # Save the user object to the database
        user.save(using=self.db)

        # Return the created user object
        return user
    
    # Define a method to create a superuser
    def create_superuser(self, user_email, password, **extra_fields):

        # Set default values for superuser fields if not provided
        extra_fields.setdefault('is_staff', True)
        # Set default for is_trusty (custom field likely)
        extra_fields.setdefault('is_trusty', True)
        # Set default for is_active
        extra_fields.setdefault('is_active', True)
        # Set default for is_superuser
        extra_fields.setdefault('is_superuser', True)

        # Check if is_staff is explicitly set to True for superuser
        if extra_fields.get('is_staff') is not True:
            # Raise ValueError if is_staff is not True
            raise ValueError(_("Superuser must have is_staff=True."))
        
        # Check if is_superuser is explicitly set to True
        if extra_fields.get('is_superuser') is not True:
            # Raise ValueError if is_superuser is not True
            raise ValueError(_("Superuser must have is_superuser=True."))
        
        # Call the create_user method to create the superuser with the specified fields
        return self.create_user(user_email, password, **extra_fields)