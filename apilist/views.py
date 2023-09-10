from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Users, UserProfile
from .serializers import UserSerializer, UserProfileSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.db import IntegrityError


class SignupView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        print("Request data:", request.data)
        # serializer.user = user_id
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']
            
            # # Check if the user already exists
            # if Users.objects.filter(username=username).exists():
            #     return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # # Create the user and hash the password
            # user = Users(username=username, password=password)
            # user.save()

            # user_name = user.username

            try:
                # Create the user and hash the password
                user = Users(username=username, password=password, email=email)
                user.save()
                user_name = user.username

                return Response({'message': 'User registered successfully.', 'username': user_name}, status=status.HTTP_201_CREATED)

            except IntegrityError as e:
                # Handle IntegrityError, which might occur due to duplicate email or username
                return Response({'error': 'User with this email or username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            # print("User email after saving:", user_email)
            # return Response({'message': 'User registered successfully.', 'username': user_name}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        try:
            user = Users.objects.get(username=username)
            print("user", user)

        except Users.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        if check_password(password, user.password):
            print("id," , request.user.id)
            # user_id = urlsafe_base64_encode(force_bytes(request.user.id))

            
            
            # print("check created", request.user.id)
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            user_name = user.username
            return Response({'user_name': user_name,'message': 'Login Successful','access_token': str(access_token), 'refresh_token': str(refresh)}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileCreateView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    # permission_classes = [IsAuthenticated]

class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    # permission_classes = [IsAuthenticated]