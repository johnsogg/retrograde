from django.db import models
from django.contrib.auth.models import User

class RetroUser(models.Model):
    user = models.OneToOneField(User)
    course = models.ForeignKey('homework.Course')
    cu_id = models.CharField(max_length=20)
    
