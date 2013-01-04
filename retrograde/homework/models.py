from django.db import models

# Create your models here.
class Homework(models.Model):
    description = models.TextField()
    pub_date = models.DateTimeField("Date published")
    due_date = models.DateField()

