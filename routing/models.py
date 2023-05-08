from django.db import models
from home.models import sathiUser
# Create your models here.
STATUS_FIElD = [
    ("C", "Complete"),
    ("I", "Incomplete"),
    ("P", "Pending"),
]
class group(models.Model):
    user = models.CharField(max_length=100)
    # status complete the travel or not
    status = models.CharField(max_length=1,choices = STATUS_FIElD)
    sathi_id = models.CharField(max_length=10, default="")
    is_feedback = models.BooleanField(default=False)
    # self.room_group_name
    group_name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    user_verification_number = models.CharField(max_length=10, default="")
    def __str__(self):
        return self.group_name

class chat (models.Model):
    user = models.CharField(max_length=500)
    message = models.TextField()
    sathi_id = models.CharField(max_length=10)
    group_name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return self.group_name

class feedback (models.Model):
    user = models.CharField(max_length=500)
    sathi_id = models.CharField(max_length=10)
    rating = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    feedback = models.TextField()
    def __str__(self):
        return self.group_name