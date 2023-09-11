# myapp/views.py

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
# from .models import UserProfile
from .serializers import CustomUserSerializer, CustomUserRegistrationSerializer, UserProfileSerializer

CustomUser = get_user_model()
UserProfileData  = get_user_model()

class CustomUserRegistration(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CustomUserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User registered successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomUserLogin(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        user = CustomUser.objects.filter(username=username).first()
        
        if user is None:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.check_password(password):
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
          
            'access token': str(refresh.access_token),
              'refresh token': str(refresh),
        }, status=status.HTTP_200_OK)
    
class UserProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)



# class UserProfileCreateView(generics.CreateAPIView):
#     queryset = UserProfileData.objects.all()
#     serializer_class = UserProfileSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class UserProfileCreateView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     def post(self, request, username, format=None):
#         # Retrieve the user based on the username or ID provided in the request
#         # username = request.data.get('username')
#         try:
#             user = CustomUser.objects.get(username=username)
#         except CustomUser.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#         create_data = {
#             "profile_picture" : request.data.get('profile_picture', None),
#             "bio" : request.data.get('bio', None),
#             "social_media_links" : request.data.get('social_media_links', None)
#         }
        
#         profile_data = {'user': user, 'data' : create_data}
#         # print("data profile", request.data, **request.data)
#         serializer = UserProfileSerializer(data=profile_data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 'message': 'User profile created successfully',
#                 'data': serializer.data
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username, format=None):
        # Retrieve the user based on the username provided in the URL
        user = get_object_or_404(CustomUser, username=username)

        # Check if a profile already exists for this user
        existing_profile = UserProfileData.objects.filter(user=user).first()
        
        if existing_profile:
            # Profile already exists, update it
            serializer = UserProfileSerializer(existing_profile, data=request.data)
        else:
            # Profile doesn't exist, create a new one
            serializer = UserProfileSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.validated_data['user'] = user  # Set the user reference explicitly
            serializer.save()
            return Response({
                'message': 'User profile created/updated successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserProfileUpdateView(generics.UpdateAPIView):
    queryset = UserProfileData.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserProfileDetailView(generics.RetrieveAPIView):
    queryset = UserProfileData.objects.all()
    serializer_class = UserProfileSerializer