from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
import uuid
import math
from django.utils import timezone

# Create your models here.

custom_username_validator = RegexValidator(
    regex=r'^[\w.@+\- ]+$',
    message='Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_/space characters.'
)

class Profile(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[custom_username_validator],  # Replace default validator
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    departement = models.CharField(
        max_length=100, null=True, blank=True, default='')
    extension = models.CharField(
        max_length=20, null=True, blank=True, default='')
    district_name = models.CharField(
        max_length=50, null=True, blank=True, default='')
    title = models.CharField(
        max_length=200, null=True, blank=True, default='')
    description_dpt = models.CharField(
        max_length=400, null=True, blank=True, default='')
    employeeId = models.CharField(max_length=50, blank=True,null=True)





class Test(models.Model):
    departement = models.CharField(max_length=100, null=True, blank=True, default='')
    date = models.DateTimeField()
