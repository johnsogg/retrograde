from django.db import models

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


class Resource(models.Model):
    homework = models.ForeignKey('Homework')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

