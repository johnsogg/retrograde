#
# views.py    - homework
#

import codecs
from datetime import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404, render
from django.utils.timezone import utc
from grade import RetroGrade, extract_score, format_results
from homework.models import Homework, Course, Submission, SubmissionFile, Score
from tempfile import mkdtemp
import os

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
        variables['due_now'] = tupleize(upcoming, request.user)
        variables['due_past'] = tupleize(past, request.user)
        variables['due_future'] = tupleize(future, request.user)
    return render(request, 'homework/course.html', variables)

def tupleize(hw_set, user):
    """
    Given a bunch of homeworks, produce a list of tuples [(hw,
    hw.get_score(user)), hw, hw.get_score(user))]
    """
    ret = []
    for hw in hw_set:
        ret.append((hw, hw.get_score(user)))
    return ret

@login_required
def view_specific_assignment(request, hw_id):
    variables = { 'user' : request.user }
    hw_set = Homework.objects.filter(id=hw_id)
    if hw_set.exists():
        hw = hw_set[0]
        variables['hw'] = hw
        variables['related'] = hw.resource_set.all()
        # has the student has submitted this homework?
        subs = hw.submission_set.filter(student=request.user)
        set_best_scores(variables, request.user, hw)
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
        this_sub = None
        if (len(files.keys()) > 0):
            # There are files, so create a submission with files.
            now = datetime.utcnow().replace(tzinfo=utc)
            sub = Submission()
            sub.homework = hw
            sub.student = request.user
            sub.submitted_date = now
            sub.score = 0
            sub.possible_score = 0
            sub.verbose_output = "verbose output..."
            sub.retrograde_output = "retrograde output..."
            sub.on_time = now < hw.due_date
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
            variables['importantMessage'] = "Got the homework"
            do_retrograde_script(sub)
            if (not sub.on_time): # cap score if late
                sub.score = min(hw.points_possible_when_late, sub.score)
                sub.save()
            variables['sub'] = sub
            this_sub = sub
            if (sub.score == sub.possible_score and sub.score > 0):
                variables['max_score'] = True
        subs = hw.submission_set.filter(student=request.user)
        variables['subs'] = subs
        set_best_scores(variables, request.user, hw)
        if (this_sub):
            return view_specific_submission(request, hw.id, this_sub.id)
    else:
        raise Http404
    return render(request, 'homework/detail.html', variables)

def set_best_scores(variables, user, hw):
    """
    This sets several variables: best_X and best_X_full for each
    language, where X is the language name. best_X is the best score
    for that language (an integer), and best_X_full is a boolean that
    tells you if you've maxed out your score.

    It also sets normal_score and extra_credit_score, both integers.

    It sets maxed_out to True if the max number of regular points are
    received.
    """
    best_java = hw.submission_set.filter(student=user, lang='java').aggregate(Max('score'))
    valj = hw.submission_set.filter(student=user, lang='java').aggregate(Max('possible_score'))
    best_py = hw.submission_set.filter(student=user, lang='py').aggregate(Max('score'))
    valp = hw.submission_set.filter(student=user, lang='py').aggregate(Max('possible_score'))
    best_cpp = hw.submission_set.filter(student=user, lang='cpp').aggregate(Max('score'))
    valc = hw.submission_set.filter(student=user, lang='cpp').aggregate(Max('possible_score'))
    variables['best_java'] = best_java['score__max'] or 0
    variables['best_java_full'] = False
    if (valj['possible_score__max'] is not None and variables['best_java'] == valj['possible_score__max']):
        variables['best_java_full'] = True
    variables['best_py'] = best_py['score__max'] or 0
    variables['best_py_full'] = False
    if (valp['possible_score__max'] is not None and variables['best_py'] == valp['possible_score__max']):
        variables['best_py_full'] = True
    variables['best_cpp'] = best_cpp['score__max'] or 0
    variables['best_cpp_full'] = False
    if (valc['possible_score__max'] is not None and variables['best_cpp'] == valc['possible_score__max']):
        variables['best_cpp_full'] = True
    best_score = max(variables['best_java'], variables['best_py'], variables['best_cpp'])
    sum_score = sum([variables['best_java'], variables['best_py'], variables['best_cpp']])
    extra_credit_score = sum_score - best_score
    variables['normal_score'] = best_score
    variables['extra_credit_score'] = extra_credit_score
    maxed_out = variables['best_java_full'] or variables['best_py_full'] or variables['best_cpp_full']
    variables['maxed_out'] = maxed_out
    score_set = Score.objects.filter(homework=hw, student=user)
    score = None
    if (len(score_set) > 0):
        score = score_set[0]
    else:
        score = Score()
        score.homework = hw
        score.student = user
    score.normal_points = best_score
    score.extra_credit_points = extra_credit_score
    score.save()
    variables['score'] = score
    
def do_retrograde_script(sub):
    """
    Runs the RetroGrade grading script. This extracts the related
    files for this homework submission to a temp dir first.
    """
    file_objects = sub.submissionfile_set.all()
    tmp = mkdtemp()
    student_files = []
    for f in file_objects:
        student_file = os.path.join(tmp, f.file_name);
        with open(student_file, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
        student_files.append(student_file)
        print "student_files is now: " + str(student_files)
    hw = sub.homework
    rg = RetroGrade(settings.RETROGRADE_INSTRUCTOR_PATH,
                    hw.instructor_dir,
                    sub.student.email,
                    student_files)
    score, possible = extract_score(rg.result_map)
    pretty = format_results(rg.result_map)
    print "Finished grading. Score: " + str(score) + " / " + str(possible)
    verbose = rg.get_verbose_log()
    sub.verbose_output = verbose
    sub.retrograde_output = pretty
    sub.lang = rg.language
    sub.flaming_error = rg.flaming_error or ''
    sub.score = score
    sub.possible_score = possible
    sub.save()
    # print pretty

@login_required
def view_specific_submission(request, hw_id, sub_id):
    variables = { 'user' : request.user }
    sub = Submission.objects.get(pk=sub_id)
    if (sub is None):
        raise Http404
    hw = Homework.objects.get(pk=hw_id)
    if (hw is None):
        raise Http404
    # ensure this user is allowed to see this submission
    if (sub.student == request.user):
        variables['sub'] = sub
        variables['hw'] = hw
    else:
        variables['importantMessage'] = 'You don\'t have permission to see that.'
    return render(request, 'homework/submission.html', variables)
