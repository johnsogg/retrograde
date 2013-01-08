#
# views.py    - homework
#

"""
This is a test.
"""

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404, render
from homework.models import Homework, Course, Submission, SubmissionFile
from datetime import datetime
from django.utils.timezone import utc

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
        variables['due_now'] = upcoming
        variables['due_past'] = past
        variables['due_future'] = future
    return render(request, 'homework/course.html', variables)
                  


@login_required
def view_specific_assignment(request, hw_id):
    variables = { 'user' : request.user }
    hw_set = Homework.objects.filter(id=hw_id)
    if hw_set.exists():
        hw = hw_set[0]
        variables['hw'] = hw
        variables['related'] = hw.resource_set.all()
        # has the student has submitted this homework?
        subs = hw.submission_set.all()
        variables['subs'] = subs
    else:
        raise Http404
    return render(request, 'homework/detail.html', variables)

@login_required
def submit_homework(request, hw_id):
    variables = { 'user' : request.user }
    hw_set = Homework.objects.filter(id=hw_id)
    if hw_set.exists():
        hw = hw_set[0]
        variables['hw'] = hw
        files = request.FILES
        print "Student " + str(request.user) + " has uploaded " + \
            str(len(files.keys())) + " files for " + str(hw.name)
        if (len(files.keys()) > 0):
            # There are files, so create a submission with files.
            now = datetime.utcnow().replace(tzinfo=utc)
            sub = Submission()
            sub.homework = hw
            sub.student = request.user
            sub.submitted_date = now
            sub.score = 0
            sub.verbose_output = "verbose output..."
            sub.retrograde_output = "retrograde output..."
            sub.save()
            print "Saved submission " + str(sub)
            for k in files.keys():
                v = files[k]
                f = SubmissionFile()
                f.submission = sub
                f.file_name = v.name
                f.uploaded_date = now
                print "\tFile: " + str(k) + " = " + str(v.name) + \
                    "(" + str(v.size) + " bytes)"
                buf = []
                for line in v:
                    buf.append(line)
                text = "".join(buf)
                f.contents = text
                f.save()
                print "Saved file upload: " + str(f)
            variables['importantMessage'] = "Got the homework"
            print("Looks like I am done!")
    else:
        raise Http404
    return render(request, 'homework/detail.html', variables)
