from homework.models import Homework, Resource, Course
from django.contrib import admin

class ResourceInline(admin.TabularInline):
    model=Resource
    extra=3
    
class HomeworkAdmin(admin.ModelAdmin):
    fields = ['name', 'course', 'description', 'pub_date', 'due_date']
    inlines = [ResourceInline]
    list_display = ('name', 'due_date')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_code')

#class ResourceAdmin(admin.ModelAdmin):
#    pass


admin.site.register(Homework, HomeworkAdmin)
admin.site.register(Course, CourseAdmin)
