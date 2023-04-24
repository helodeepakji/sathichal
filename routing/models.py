from django.db import models
from home.models import sathiUser
# Create your models here.
class group(models.Model):
    # jo user add hua
    added_user = models.CharField(max_length=100)
    # jis user ne add kiya / jis user nei confirm kiya
    added_by_user = models.CharField(max_length=100)
    # self.room_group_name
    group_name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
