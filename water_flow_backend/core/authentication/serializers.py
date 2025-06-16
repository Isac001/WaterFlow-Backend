# Django imports
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

# Import only your custom user model.
from apps.user.models import User


class TokenPairSerializer(TokenObtainPairSerializer):
    """
    This serializer obtains the token pair (refresh and access) for the custom 
    user model.

    It authenticates the user based on email and password and adds
    user information to the token.
    """

    # Overrides the get_token method to add custom claims.
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Adds basic user claims to the token.
        token['user_name'] = user.user_name
        token['user_email'] = user.user_email
        token['user_cpf'] = user.user_cpf
        token['is_staff'] = user.is_staff

        return token

    # Overrides the main validation method.
    def validate(self, attrs):
        # Django's authenticate uses the USERNAME_FIELD ('user_email') from your model.
        # By default, it expects 'username', so we pass the email to that parameter.
        user = authenticate(
            request=self.context.get('request'),
            username=attrs.get('user_email'),
            password=attrs.get('password')
        )

        # If authentication fails, raise a clear error.
        if not user:
            raise serializers.ValidationError("Invalid credentials. Check your email and password.")

        # Check if the user is active.
        if not user.is_active:
            raise serializers.ValidationError("This user account is inactive.")

        # If all validations pass, the parent class handles token generation.
        data = super().validate(attrs)
        
        return data


# Serializer for the refresh token
class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    
    # Define a field for the refresh token
    refresh = serializers.CharField()

    # Define the validation method
    def validate(self, attrs):
        # Get the refresh token from the request data
        refresh = RefreshToken(attrs['refresh'])

        # Create a new pair of access and refresh tokens
        data = {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

        # Return the new tokens
        return data
