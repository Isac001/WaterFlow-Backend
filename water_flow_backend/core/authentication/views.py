
# Django imports
from rest_framework import filters, generics, response, status
from rest_framework.permissions import IsAuthenticated

# Third-party imports
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# First-party imports
from core.authentication.serializers import (
    CustomTokenRefreshSerializer,
    TokenPairSerializer,
)


# Token Obter View  
class TokenPairObtain(TokenObtainPairView):

    serializer_class = TokenPairSerializer

# Token Refresh View
class CustomTokenRefreshView(TokenRefreshView):
    
    serializer_class = CustomTokenRefreshSerializer


# Logout View
class Logout(generics.CreateAPIView):

    # If the user is authenticated, they will have access to the method
    permission_classes = (IsAuthenticated, )

    # Overriding the method
    def post(self, request):

        try:
            
            # Blacklist all outstanding tokens
            tokens = OutstandingToken.objects.filter(user_id=request.user.id)

            # For each token in the list blacklist it in the database
            for token in tokens:
                
                # Blacklist the token
                t, _ = BlacklistedToken.objects.get_or_create(token=token)

            # Return a response with status HTTP 205 Reset Content
            return response.Response(status=status.HTTP_205_RESET_CONTENT)

        except TokenError:
            
            # Return a response with status HTTP 401 Unauthorized
            return response.Response(status=status.HTTP_401_UNAUTHORIZED)
    


    