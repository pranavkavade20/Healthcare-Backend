from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db import IntegrityError

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer
)
from .utils import success_response, error_response


class UserRegistrationView(APIView):
    """
    API endpoint for user registration.
    POST: Create a new user account.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Register a new user with name, email, and password.
        
        Request body:
        {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "SecurePass123!",
            "password_confirm": "SecurePass123!"
        }
        """
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            
            if serializer.is_valid():
                user = serializer.save()
                
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                
                response_data = {
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }
                
                return success_response(
                    data=response_data,
                    message="User registered successfully",
                    status_code=status.HTTP_201_CREATED
                )
            
            return error_response(
                message="Validation failed",
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        except IntegrityError:
            return error_response(
                message="A user with this email already exists",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            return error_response(
                message="An error occurred during registration",
                details=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserLoginView(APIView):
    """
    API endpoint for user login.
    POST: Authenticate user and return JWT tokens.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Log in a user and return JWT tokens.
        
        Request body:
        {
            "email": "john@example.com",
            "password": "SecurePass123!"
        }
        """
        try:
            serializer = UserLoginSerializer(data=request.data)
            
            if not serializer.is_valid():
                return error_response(
                    message="Validation failed",
                    details=serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            # Authenticate user
            user = authenticate(
                request,
                username=email,  # We use email as username
                password=password
            )
            
            if user is None:
                return error_response(
                    message="Invalid credentials",
                    details="The email or password you entered is incorrect",
                    status_code=status.HTTP_401_UNAUTHORIZED
                )
            
            if not user.is_active:
                return error_response(
                    message="Account disabled",
                    details="This account has been disabled",
                    status_code=status.HTTP_403_FORBIDDEN
                )
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            response_data = {
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }
            
            return success_response(
                data=response_data,
                message="Login successful",
                status_code=status.HTTP_200_OK
            )
        
        except Exception as e:
            return error_response(
                message="An error occurred during login",
                details=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )