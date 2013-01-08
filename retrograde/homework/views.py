#
# views.py    - homework
#

"""
This is a test.
"""

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404, render
from homework.models import Homework, Course

# def index(request):
#     """
#     Word! Now I can document things and have it show up on some admin
#     documentation thing. Zany.
#     """

#     greeting = "This is a fantastic greeting for Sputnik"
#     return render(request, 'homework/index.html', {
#     return render_to_response("homework/index.html", {"greeting" : greeting})

# def specific(request, hw_id):
#     p = get_object_or_404(Homework, pk=hw_id)
#     return render_to_response('homework/detail.html', {'homework': p})

@login_required
def course(request, course_id):
    course = Course.objects.get(id=course_id)
    variables = {'user' : request.user }
    if (course):
        variables['course'] = course
        homeworks = Homework.objects.filter(course_id=course.id)
        upcoming = filter(Homework.is_now, homeworks)
        past = filter(Homework.is_past, homeworks)
        future = filter(Homework.is_future, homeworks)
    return render(request, 'homework/course.html',
                  { 'user' : request.user,
                    'course' : course,
                    'due_now' : upcoming,
                    'due_past' : past,
                    'due_future' : future,
                    })

