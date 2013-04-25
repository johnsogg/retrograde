from django.contrib.auth.models import User
from django.db import models
from datetime import datetime, timedelta
from django.utils.timezone import utc


class Course(models.Model):
    name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=9)
    description = models.TextField()
    home_page = models.URLField()

    def __unicode__(self):
        return self.course_code

class TeachingAssistant(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course)

    def __unicode__(self):
        return self.name

class Homework(models.Model):
    name = models.CharField(max_length=100, 
                            help_text='Human-readable name of assignment')
    instructor_dir = models.CharField(max_length=40, 
                                      help_text='Directory on disk with this assignment\'s description-common.json')
    course = models.ForeignKey(Course)
    description = models.TextField()
    points_possible = models.IntegerField()
    points_possible_when_late = models.IntegerField()
    pub_date = models.DateTimeField("Date published")
    due_date = models.DateTimeField()

    def __unicode__(self):
        return self.name

    def get_score(self, user):
        ret = None
        score_set = Score.objects.filter(homework=self, student=user)
        if (len(score_set) > 0):
            ret = score_set[0]
        return ret

    def is_past(self):
        ret = False
        if self.get_now() > self.due_date:
            ret = True
        return ret

    def is_now(self):
        ret = False
        if not self.is_past() and self.is_future():
            td = timedelta(7)
            then = self.due_date - td
            ret = self.get_now() > then
        return ret
    
    def is_future(self):
        ret = False
        if self.get_now() <= self.due_date:
            ret = True
        return ret

    def get_now(self):
        return datetime.utcnow().replace(tzinfo=utc)

class Submission(models.Model):
    homework = models.ForeignKey(Homework)
    student = models.ForeignKey(User)
    submitted_date = models.DateTimeField("Date Submitted")
    score = models.IntegerField()
    possible_score = models.IntegerField()
    lang = models.CharField(max_length=10)
    verbose_output = models.TextField()
    retrograde_output = models.TextField()
    on_time = models.BooleanField()
    flaming_error = models.CharField(max_length=20)

    def __unicode__(self):
        late = ""
        if not self.on_time:
            late = "(late)"
        return "Submission '%s' (%d/%d) in %s %s" % (self.homework.name, self.score, self.possible_score, self.lang, late)

class SubmissionFile(models.Model):
    submission = models.ForeignKey(Submission)
    contents = models.TextField()
    file_name = models.CharField(max_length=100)
    uploaded_date = models.DateTimeField("Date Uploaded")

class Resource(models.Model):
    homework = models.ForeignKey(Homework)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Score(models.Model):
    """
    A score is _derived_ data that relates the student, homework, and
    submission tables. It is updated every time the student turns
    something in. It is derived to speed up and simplify loading of
    pages that display summary statistics.
    """
    homework = models.ForeignKey(Homework)
    student = models.ForeignKey(User)
    normal_points = models.IntegerField()
    extra_credit_points = models.IntegerField()

    def is_maxed_out(self):
        return self.normal_points == self.normal_points_possible

    def __unicode__(self):
        return str(self.normal_points) + " regular points earned, plus " + str(self.extra_credit_points) + " extra credit"

class Exam(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course)
    max_points = models.IntegerField()
    exam_date = models.DateField()
    
    def __unicode__(self):
        return self.name + " (" + self.course.course_code + ")"

class ExamResult(models.Model):
    exam = models.ForeignKey(Exam)
    student = models.ForeignKey(User)
    score = models.IntegerField()
    ta = models.ForeignKey(TeachingAssistant, null=True)

    def __unicode__(self):
        return self.student.first_name + " " + self.student.last_name + "<" + self.student.get_profile().cu_id + ">: " + str(self.score) + " points"

class ExtraCredit(models.Model):
    student = models.ForeignKey(User)
    score = models.IntegerField()
    why = models.TextField()

    def __unicode__(self):
        return str(self.score) + " points for " + str(self.student) + ". Reason: " + str(self.why)

class Grade(models.Model):
    student = models.ForeignKey(User)
    score_hw = models.IntegerField()
    score_exam = models.IntegerField()
    score_extra = models.IntegerField()
    score_final = models.IntegerField()
    course = models.ForeignKey(Course)
    grade = models.CharField(max_length=2)
    remark = models.TextField()

    def __unicode__(self):
        return self.course.course_code + "\t" + \
            self.student.last_name + "\t" + \
            self.student.first_name + "\t" + \
            self.student.get_profile().cu_id + "\t" + \
            self.student.email + "\t" + \
            str(self.score_hw) + "\t" + \
            str(self.score_exam) + "\t" + \
            str(self.score_extra) + "\t" + \
            str(self.score_final) + "\t" + \
            str(self.grade) + "\t" + \
            str(self.remark);


