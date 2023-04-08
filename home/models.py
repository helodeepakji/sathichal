from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class sathiUser(AbstractUser):
    phone = models.CharField(max_length=15)
    aadhaarno = models.CharField(max_length=12)
    pass