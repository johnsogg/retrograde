from homework.models import Homework, Resource, Course, Submission, Exam, ExamResult, TeachingAssistant

from account.models import RetroUser

from django.contrib import admin

class PersonInline(admin.TabularInline):
    model = RetroUser
    raw_id_fields = ("cu_id",)

class ResourceInline(admin.TabularInline):
    model=Resource
    extra=3
    
class HomeworkAdmin(admin.ModelAdmin):
    fields = ['name', 'instructor_dir', 'course', 'points_possible', 'points_possible_when_late', 'description', 'pub_date', 'due_date']
    inlines = [ResourceInline]
    list_display = ('name', 'due_date', 'course')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_code')

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('homework', 'student', 'score', 'possible_score', 'lang', 'submitted_date')

class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'max_points', 'exam_date')

class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('exam', 'student', 'score')

admin.site.register(Homework, HomeworkAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(ExamResult, ExamResultAdmin)
admin.site.register(TeachingAssistant)
