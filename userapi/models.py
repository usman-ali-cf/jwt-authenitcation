from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager


GENDER_CHOICES = (
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other")
)


# Create your models here.
class AuthUser(AbstractBaseUser):
    name = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(max_length=50, null=False, unique=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=30, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    is_admin = models.BooleanField(default=False, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
