from django.db import models
from django.contrib.auth.models import User
from .utils import user_directory_path

# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    Photo=models.ImageField(upload_to=user_directory_path,null=True)
    bio=models.CharField(max_length=140,blank=True)
    phone_number=models.CharField(max_length=10,blank=True) 
    def __str__(self):
        return f'{self.user.username}\'s profile'
    