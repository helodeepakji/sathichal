from django.db import models
from home.models import sathiUser
# Create your models here.
STATUS_FIElD = [
    ("C", "Complete"),
    ("I", "Incomplete"),
    ("P", "Pending"),
]
class group(models.Model):
    # jo user add hua
    # added_user = models.CharField(max_length=100)
    # jis user ne add kiya / jis user nei confirm kiya
    user = models.CharField(max_length=100)
    # status complete the travel or not
    status = models.CharField(max_length=1,choices = STATUS_FIElD)
    sathi_id = models.CharField(max_length=10)
    # self.room_group_name
    group_name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return self.group_name
