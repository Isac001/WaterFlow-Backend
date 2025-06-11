# Django and Python Imports
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.db.models import Q

# Project Imports
from .models import User


# Define a serializer for the User model (general purpose)
class UserSerializer(serializers.ModelSerializer):

    # Define metadata options for the serializer
    class Meta:

        # Specify the model that this serializer will work with
        model = User

        # Define the list of fields to include in the serialized output
        fields = ['id', 'user_name', 'user_email', 'user_cpf', 'password']

# Define a serializer for creating new User instances
class UserCreateSerializer(serializers.ModelSerializer):

    # Define metadata options for the serializer
    class Meta:

        # Specify the model that this serializer will work with
        model = User

        # Define the list of fields to include for user creation
        fields = ['id', 'user_name', 'user_email', 'user_cpf', 'password']

    # Override the create method to handle user creation logic
    def create(self, validated_data):

        # Extract the password from validated_data, or set to None if not present
        password = validated_data.pop('password', None)

        # Create a new User object with the remaining validated data and the extracted password
        user = User.objects.create(**validated_data, password=password)

        # Return the created user instance
        return user
    
# Define a serializer for updating existing User instances
class UserUpdateSerializer(serializers.ModelSerializer):

    # Define metadata options for the serializer
    class Meta:

        # Specify the model that this serializer will work with
        model = User

        # Define the list of fields that can be updated
        fields = ['id', 'user_name', 'user_email', 'user_cpf', 'password']

    # Override the update method to handle user update logic
    def update(self, instance, validated_data):

        # Update the user_name field if provided in validated_data, otherwise keep the existing value
        instance.user_name = validated_data.get('user_name', instance.user_name)

        # Save the updated user instance to the database
        instance.save()

        # Return the updated user instance
        return instance
    
# Define a custom serializer for obtaining JWT token pairs
class CustomTokenObtainPairSerializer(serializers.Serializer):

    # Define an email field for user input
    user_email = serializers.EmailField()

    # Define a password field for user input, write-only means it's not included in response
    password = serializers.CharField(write_only=True)

    # Define a method to authenticate the user based on provided attributes
    def authenticate_user(self, attrs):

        # Get the email from the input attributes
        email = attrs.get('user_email')

        # Get the password from the input attributes
        password = attrs.get('password')

        # Get the currently active User model
        User = get_user_model()

        # Attempt to retrieve the user by email
        user = User.objects.filter(Q(user_email=email)).first()

        # Check if the user exists and the provided password is correct
        if user and user.check_password(password):

            # Return True and the user object if authentication is successful
            return True, user
        
        # Return False and None if authentication fails
        return False, None
    
    # Define a method to generate token data for a given user
    def get_token_data(self, user):

        # Generate a refresh token for the user
        refresh = RefreshToken.for_user(user)
        
        # Return a dictionary containing the refresh and access tokens
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

    # Override the validate method to perform authentication and token generation
    def validate(self, user): # Note: `user` parameter here is actually `attrs` from DRF `validate` method signature

        # Authenticate the user using the validated data from the request
        status, user_obj = self.authenticate_user(self.validated_data) # Renamed `user` to `user_obj` for clarity

        # Check if authentication failed
        if not status:

            # Raise a validation error if authentication is unsuccessful
            raise serializers.ValidationError("Please provide a valid email and password.")
        
        # Check if user object was not found (though `status` should also cover this)
        if not user_obj:

            # Raise a validation error if the user is not found
            raise serializers.ValidationError("User not found.")
        
        # If authentication is successful, return the generated token data
        return self.get_token_data(user_obj)