from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.db.models import Q


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'user_name', 'user_email', 'user_cpf', 'password']

class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'user_name', 'user_email', 'user_cpf', 'password']

    def create(self, validated_data):

        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data, password=password)
        return user
    
class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'user_name', 'user_email', 'user_cpf', 'password']

    def update(self, instance, validated_data):

        instance.user_name = validated_data.get('user_name', instance.user_name)
        instance.save()
        return instance
    
class CustomTokenObtainPairSerializer(serializers.Serializer):

    user_email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def authenticate_user(self, attrs):

        email = attrs.get('user_email')
        password = attrs.get('password')

        User = get_user_model()

        user = User.objects.filter(Q(user_email=email)).first()

        if user and user.check_password(password):

            return True, user
        
        return False, None
    
    def get_token_data(self, user):

        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

    def validate(self, user):

        status, user = self.authenticate_user(self.validated_data)

        if not status:

            raise serializers.ValidationError("Please provide a valid email and password.")
        
        if not user:

            raise serializers.ValidationError("User not found.")
        
        return self.get_token_data(user)

