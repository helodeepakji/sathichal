from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

GENDER_FIElD = [
    ("M", "Male"),
    ("F", "Female"),
    ("O", "Other"),
]

class sathiUser(AbstractUser):
    gender =  models.CharField(max_length=1,choices = GENDER_FIElD)
    phone = models.CharField(max_length=15)
    dob = models.DateField(default="2000-01-01")
    aadhaarno = models.CharField(max_length=12)
    pass

class Contact(models.Model):
    name = models.CharField(max_length=75)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=15)
    question = models.TextField()