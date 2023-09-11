# myapp/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    social_media_links = models.URLField(blank=True)


class UserProfileData(models.Model):
    user = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE, blank=True, unique=True, related_name='user_profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    social_media_links = models.URLField(blank=True)

    objects = models.Manager()  # Add this line to define the custom manager

    def __str__(self):
        return str(self.user)