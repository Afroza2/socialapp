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



class SignupView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            # Check if the user already exists
            if Users.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create the user and hash the password
            user = Users(username=username, password=password)
            user.save()
            
            return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = Users.objects.get(username=username)
            print("user", user)

        except Users.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        if check_password(password, user.password):
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            return Response({'message': 'Login Successful','access_token': str(access_token), 'refresh_token': str(refresh)}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)
    

class UserProfileListCreateView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
