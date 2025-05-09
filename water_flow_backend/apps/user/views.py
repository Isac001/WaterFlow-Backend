# Django Imports
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

# Project Imports
from .models import User
from .serializers import *

class CustomTokenObtainPairVie(APIView):

    def post(self, request):

        serializer = CustomTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():

            return response.Response(serializer.validated_data, status=status.HTTP_200_OK)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomTokenRefreshView(TokenRefreshView):
    
    pass

class UserListView(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request):

        try:
            users = self.get_queryset()
            serializers = self.serializer_class(users, many=True)
            return response.Response(serializers.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return response.Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
        except ObjectDoesNotExist:

            return response.Response(data={"message": "No users found"}, status=status.HTTP_404_NOT_FOUND)
      
class UserDetailView(generics.RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request, pk):

        try:
            serializer = self.serializer_class(self.queryset.get(pk=pk))
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        
        except ObjectDoesNotExist:
            return response.Response(data={"message": "The user does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return response.Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
class UserCreateView(generics.CreateAPIView):

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request):

        try:

            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():

                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except IntegrityError:

            return response.Response(data={"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        except ValidationError as e:

            return response.Response(f'ERROR: {str(e)}', status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return response.Response({"ERROR": f"Internal server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserUpdateView(generics.RetrieveUpdateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def update(self, request, pk):

        try:

            user = get_object_or_404(User, pk=pk)
            serializer = self.serializer_class(user, data=request.data, partial=True)

            if serializer.is_valid():

                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_200_OK)
            
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except IntegrityError:

            return response.Response(data={"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        except ValidationError as e:

            return response.Response(f'ERROR: {str(e)}', status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return response.Response({"ERROR": f"Internal server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserDeleteView(generics.RetrieveDestroyAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def delete(self, request, pk):

        try:

            user = get_object_or_404(User, pk=pk)
            user.delete()
            return response.Response(data= {"message": "User deleted"},status=status.HTTP_204_NO_CONTENT)

        except IntegrityError:

            return response.Response(data={"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        except ValidationError as e:

            return response.Response(f'ERROR: {str(e)}', status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return response.Response({"ERROR": f"Internal server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
