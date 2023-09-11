from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager

# Create your models here.

ROLE_CHOICES = (
    ("user", "System User"),
    ("admin", "System Admin"),
)

GENDER_CHOICES = (
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other")
)


class Role(models.Model):
    user_role = models.CharField(choices=ROLE_CHOICES, max_length=30, null=False, default="user")
    description = models.CharField(max_length=100, null=True)

    class Meta:
        pass

    def __str__(self):
        return self.user_role + " : " + self.description


class AuthUser(AbstractBaseUser):
    name = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(max_length=50, null=False, unique=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=30, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
