# Django and Python Imports
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, response, status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from builtins import Exception
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

# Project Imports
from .models import User
from .serializers import *

# Define a view for listing all users
class UserListView(generics.ListAPIView):

    # Specify that only authenticated users can access this view
    permission_classes = (IsAuthenticated,)

    # Specify the serializer class to be used for User objects
    serializer_class = UserSerializer

    # Define the queryset to retrieve all User objects
    queryset = User.objects.all()

    # Define the handler for GET requests
    def get(self, request):

        # Start a try block to handle potential exceptions
        try:
            # Get the queryset of users
            users = self.get_queryset()

            # Serialize the list of users
            serializers = self.serializer_class(users, many=True)

            # Return the serialized user data with a 200 OK status
            return response.Response(serializers.data, status=status.HTTP_200_OK)
        
        # Catch any generic exception
        except Exception as e:

            # Return the string representation of the error with a 400 Bad Request status
            return response.Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
        # Catch ObjectDoesNotExist exception specifically (though get_queryset usually doesn't raise this for empty lists)
        except ObjectDoesNotExist:

            # Return a message indicating no users were found with a 404 Not Found status
            return response.Response(data={"message": "No users found"}, status=status.HTTP_404_NOT_FOUND)
      
# Define a view for retrieving details of a single user
class UserDetailView(generics.RetrieveAPIView):

    # Specify that only authenticated users can access this view
    permission_classes = (IsAuthenticated,)

    # Specify the serializer class to be used for User objects
    serializer_class = UserSerializer

    # Define the queryset to retrieve all User objects (actual filtering by pk happens in get)
    queryset = User.objects.all()

    # Define the handler for GET requests, taking primary key (pk) as an argument
    def get(self, request, pk):

        # Start a try block to handle potential exceptions
        try:

            # Serialize the user object retrieved by primary key
            serializer = self.serializer_class(self.queryset.get(pk=pk))

            # Return the serialized user data with a 200 OK status
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        
        # Catch ObjectDoesNotExist exception if the user is not found
        except ObjectDoesNotExist:

            # Return a message indicating the user does not exist with a 404 Not Found status
            return response.Response(data={"message": "The user does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        # Catch any other generic exception
        except Exception as e:

            # Return the string representation of the error with a 400 Bad Request status
            return response.Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
# Define a view for creating new users
class UserCreateView(generics.CreateAPIView):

    # Specify the serializer class to be used for creating User objects
    serializer_class = UserCreateSerializer 

    # Define the queryset (used by generic views, though post is overridden here)
    queryset = User.objects.all()

    # Define the handler for POST requests
    def post(self, request):

        # Start a try block to handle potential exceptions
        try:

            # Instantiate the serializer with request data
            serializer = self.serializer_class(data=request.data)

            # Check if the serializer data is valid
            if serializer.is_valid():

                # Save the new user object
                serializer.save()

                # Return the serialized data of the created user with a 201 Created status
                return response.Response(serializer.data, status=status.HTTP_201_CREATED)
            
        # Catch IntegrityError if, for example, a unique constraint is violated
        except IntegrityError:

            # Return a message indicating the user already exists with a 400 Bad Request status
            return response.Response(data={"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Catch ValidationError if form/serializer validation fails
        except ValidationError as e:

            # Return the error message with a 400 Bad Request status
            return response.Response(f'ERROR: {str(e)}', status=status.HTTP_400_BAD_REQUEST)
        
        # Catch any other generic exception
        except Exception as e:

            # Return a generic internal server error message with a 500 Internal Server Error status
            return response.Response({"ERROR": f"Internal server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Define a view for retrieving and updating a user
class UserUpdateView(generics.RetrieveUpdateAPIView):

    # Specify that only authenticated users can access this view
    permission_classes = (IsAuthenticated,)

    # Specify the serializer class to be used (consider UserUpdateSerializer if different)
    serializer_class = UserUpdateSerializer

    # Define the queryset to retrieve all User objects
    queryset = User.objects.all()

    # Override the update method (handles both PUT and PATCH by default in RetrieveUpdateAPIView)
    def update(self, request, pk): # Note: `pk` is passed from URL

        # Start a try block to handle potential exceptions
        try:

            # Get the user object to be updated, or raise 404 if not found
            user = get_object_or_404(User, pk=pk)

            # Instantiate the serializer with the user instance and request data, allowing partial updates
            serializer = self.serializer_class(user, data=request.data, partial=True)

            # Check if the serializer data is valid
            if serializer.is_valid():

                # Save the updated user object
                serializer.save()

                # Return the serialized data of the updated user with a 200 OK status
                return response.Response(serializer.data, status=status.HTTP_200_OK)
            
            # If serializer data is invalid, return errors with a 400 Bad Request status
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Catch IntegrityError
        except IntegrityError:

            # Return a message indicating the user already exists (e.g., if trying to change email to an existing one)
            return response.Response(data={"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Catch ValidationError
        except ValidationError as e:

            # Return the error message with a 400 Bad Request status
            return response.Response(f'ERROR: {str(e)}', status=status.HTTP_400_BAD_REQUEST)
        
        # Catch any other generic exception
        except Exception as e:
            # Return a generic internal server error message with a 500 Internal Server Error status
            return response.Response({"ERROR": f"Internal server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# Define a view for retrieving and deleting a user
class UserDeleteView(generics.RetrieveDestroyAPIView):

    # Specify that only authenticated users can access this view
    permission_classes = (IsAuthenticated,)

    # Specify the serializer class (used for retrieving before deleting)
    serializer_class = UserSerializer

    # Define the queryset to retrieve all User objects
    queryset = User.objects.all()

    # Override the delete method (handles DELETE requests)
    def delete(self, request, pk): 

        # Start a try block to handle potential exceptions
        try:

            # Get the user object to be deleted, or raise 404 if not found
            user = get_object_or_404(User, pk=pk)

            # Delete the user object
            user.delete()

            # Return a message indicating successful deletion with a 204 No Content status
            return response.Response(data= {"message": "User deleted"},status=status.HTTP_204_NO_CONTENT)

        # Catch IntegrityError (less likely on delete unless protected by foreign keys)
        except IntegrityError:

            # Return a message (context might be specific, e.g. cannot delete user with related data)
            return response.Response(data={"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST) # Message might need adjustment for delete context
        
        # Catch ValidationError
        except ValidationError as e:

            # Return the error message with a 400 Bad Request status
            return response.Response(f'ERROR: {str(e)}', status=status.HTTP_400_BAD_REQUEST)
        
        # Catch any other generic exception
        except Exception as e:
            # Return a generic internal server error message with a 500 Internal Server Error status
            return response.Response({"ERROR": f"Internal server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


