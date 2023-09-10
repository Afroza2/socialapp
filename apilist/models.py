from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.


class Users(models.Model):
    # id = models.IntegerField( primary_key=True)
    username = models.CharField(max_length=50, primary_key=True)
    email = models.EmailField()
    password = models.CharField(max_length=128) 

    def save(self, *args, **kwargs):
        # Hash the password before saving to the database
        self.password = make_password(self.password)
        super(Users, self).save(*args, **kwargs)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
    
class UserProfile(models.Model):
    user = models.OneToOneField(Users,null=True, on_delete=models.CASCADE, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    social_media_links = models.URLField(blank=True)

    # def __str__(self):
    #     return self.user.id