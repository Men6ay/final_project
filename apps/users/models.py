from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import *
import jwt
from django.conf import settings


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise TypeError("Please, enter your email.")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


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
    email = models.EmailField(
    )

    is_active = models.BooleanField(default=False)

    objects = MyUserManager()

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')
        return token

    def __str__(self):
        return f"{self.username} -- {self.gender}"
