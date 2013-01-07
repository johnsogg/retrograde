from django.db import models
from django.contrib.auth.models import User

class RetroUser(models.Model):
    user = models.OneToOneField(User)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)

