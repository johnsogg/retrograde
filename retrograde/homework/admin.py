from homework.models import Homework, Resource, Course, Submission
from django.contrib import admin

class ResourceInline(admin.TabularInline):
    model=Resource
    extra=3
    
class HomeworkAdmin(admin.ModelAdmin):
    fields = ['name', 'course', 'description', 'pub_date', 'due_date']
    inlines = [ResourceInline]
    list_display = ('name', 'due_date', 'course')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_code')

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('homework', 'student', 'score', 'possible_score', 'lang', 'submitted_date')


admin.site.register(Homework, HomeworkAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Submission, SubmissionAdmin)
