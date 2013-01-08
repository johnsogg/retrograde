from django.db import models
from datetime import date, timedelta

class Course(models.Model):
    name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=9)
    description = models.TextField()
    home_page = models.URLField()

    def __unicode__(self):
        return self.course_code

class Homework(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey('Course')
    description = models.TextField()
    pub_date = models.DateTimeField("Date published")
    due_date = models.DateField()

    def __unicode__(self):
        return self.name

    def is_past(self):
        ret = False
        if date.today() > self.due_date:
            ret = True
        return ret

    def is_now(self):
        ret = False
        if self.is_future:
            td = timedelta(7)
            then = self.due_date - td
            ret = date.today() > then
        return ret
    
    def is_future(self):
        ret = False
        if date.today() <= self.due_date:
            ret = True
        return ret


class Resource(models.Model):
    homework = models.ForeignKey('Homework')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

