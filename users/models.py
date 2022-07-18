# AbstractUser is used if the standard user model that Django comes with is ok.
# AbstractBaseUser is used if you want to start from scratch to create a new user model.
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):

    STATUS = (
        ('regular', 'regular'),
        ('subscriber', 'subscriber'),
        ('moderator', 'moderator'),
        ('staff', 'staff'),
        ('administrator', 'administrator'),
    )
    
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=STATUS, default='regular')
    description = models.TextField("Description", max_length=600, default='', blank=True)

    def __str__(self):
        return self.username