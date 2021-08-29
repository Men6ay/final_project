from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    GENDER_CHOICES = (
        ('m', 'Men'),
        ('f', 'Female'),
    )
    username = models.CharField(
        max_length=255, unique=True
        )
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=255
        )
    age = models.PositiveIntegerField(
        default=0
        )
    email= models.EmailField(
    )

    def __str__(self):
        return f"{self.username} -- {self.gender}"
    
