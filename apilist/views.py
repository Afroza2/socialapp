# myapp/views.py

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import CustomUser, UserProfileData, Post, Comment, Like, Share
from django.shortcuts import get_object_or_404
from django.views import View
# from .models import UserProfile
from .serializers import CustomUserSerializer, CustomUserRegistrationSerializer, UserProfileSerializer, PostSerializer, CommentSerializer, LikeSerializer, ShareSerializer

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


class UserProfileCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        self.user_id = kwargs.get('user_id')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Retrieve the user based on the user_id provided in the URL
        # user = get_object_or_404(CustomUser, id=self.user_id)

        # Check if a profile already exists for this user
        existing_profile = UserProfileData.objects.filter(id=self.user_id).first()

        if existing_profile:
            # Profile already exists, update it
            serializer = UserProfileSerializer(existing_profile, data=request.data)
        else:
            # Profile doesn't exist, create a new one
            serializer = UserProfileSerializer(data=request.data)

        if serializer.is_valid():
            # serializer.validated_data['user'] = user  # Set the user reference explicitly
            serializer.save()
            return Response({
                'message': 'User profile created/updated successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileUpdateView(APIView):
    def patch(self, request):
        # Retrieve the user's profile
        try:
            user_profile = UserProfileData.objects.get(user=request.user)
        except UserProfileData.DoesNotExist:
    # If the profile doesn't exist, create a new one
            user_profile = UserProfileData(user=request.user)

        # Serialize and partially update profile data
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileDetailView(generics.RetrieveAPIView):
    queryset = UserProfileData.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class ConnectView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        try:
            target_user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Add the target_user to the current user's connections
        request.user.connections.add(target_user)
        return Response({'message': 'Connected successfully.'}, status=status.HTTP_201_CREATED)
    

class ConnectionListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # def dispatch(self, request, *args, **kwargs):
    #     self.user_id = kwargs.get('user_id')
    #     return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Get connections of the specified user
        connections = user.connections.all()
        serializer = CustomUserSerializer(connections, many=True)  # UserSerializer for displaying user details
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class RemoveFriendView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, user_id, friend_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            friend = CustomUser.objects.get(id=friend_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User or friend not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the friend exists in the user's friend list
        if friend in user.connections.all():
            # Remove the friend from the user's friend list
            user.connections.remove(friend)
            return Response({'message': 'Friend removed successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Friend not found in your friend list.'}, status=status.HTTP_404_NOT_FOUND)
    
class ConnectionUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    

# class FeedView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         # Get posts from the user's connections
#         connections = request.user.connections.all()
#         posts = Post.objects.filter(user__in=connections).order_by('-created_at')
#         serializer = PostSerializer(posts, many=True)  # PostSerializer for displaying posts
#         return Response(serializer.data)


class CreatePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        text = request.POST.get('content', '')
        image = request.FILES.get('pic')

        if text or image:
            post = Post(user=user, content=text, pic=image)
            post.save()
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Both text and image are required.'}, status=status.HTTP_400_BAD_REQUEST)

    
    
class UserFeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        posts = Post.objects.filter(user=user)  # Get posts associated with the user
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class LikePostView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(pk=post_id)
        serializer.save(user=self.request.user, post=post)

class CommentPostView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(pk=post_id)
        serializer.save(user=self.request.user, post=post)

class SharePostView(generics.CreateAPIView):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(pk=post_id)
        serializer.save(user=self.request.user, post=post)





