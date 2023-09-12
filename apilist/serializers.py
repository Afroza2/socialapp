# myapp/serializers.py

from rest_framework import serializers
from .models import CustomUser, UserProfileData, Post,  Comment,Like, Share 

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email',  'profile_picture', 'bio', 'social_media_links')

class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileData
        fields = ('id','profile_picture', 'bio', 'social_media_links')





class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id',  'content', 'pic', 'created_at')
        # fields = '__all__'

    # def create(self, validated_data):
    #     # When creating a post, associate it with the current user
    #     validated_data['user'] = self.context['request'].user
    #     return super().create(validated_data)

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = '__all__'