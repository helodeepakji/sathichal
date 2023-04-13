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
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=50, default="")
    profile_pic = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    pass

class Contact(models.Model):
    name = models.CharField(max_length=75)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=15)
    question = models.TextField()
    def __str__(self):
        return self.email