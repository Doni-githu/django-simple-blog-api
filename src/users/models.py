from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    name = models.CharField(max_length=225)
    email = models.EmailField(max_length=225, unique=True)
    password = models.CharField(max_length=225)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']