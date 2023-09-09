from rest_framework import serializers
from .models import Users, UserProfile
from django.contrib.auth import get_user_model

Users = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ( 'username','email', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'bio', 'social_media_links')
