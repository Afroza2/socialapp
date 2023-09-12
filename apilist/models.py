# myapp/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image

class CustomUser(AbstractUser):
    # id = models.AutoField() 
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    social_media_links = models.URLField(blank=True)
    connections = models.ManyToManyField('self', symmetrical=False, related_name='connected_to')


class UserProfileData(models.Model):
    user = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE, blank=True, unique=True, related_name='user_profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    social_media_links = models.URLField(blank=True)

    objects = models.Manager()  # Add this line to define the custom manager

    def __str__(self):
        return str(self.user)
    
class Post(models.Model):
    # id = models.AutoField(primary_key=True) 
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    # profile = models.OneToOneField(UserProfileData, null=True, on_delete=models.CASCADE, blank=True, unique=True, related_name='user_profile')
    content = models.TextField(blank=True, null=True)
    pic =  models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username}"

    
class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Share(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    
