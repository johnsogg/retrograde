#
# views.py    - account
#

from django.contrib.auth.decorators import login_required
from django.forms.util import ErrorList
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, render
from homework.models import *
from account.forms import CreateAccountForm
from account.forms import LogInForm
from account.forms import LookupForm
from django.contrib.auth.models import User
from account.models import *
from django.contrib.auth import authenticate, login, logout

def index(request):
    if request.user.is_authenticated():
        variables = {'user' : request.user}
        try :
            course = request.user.get_profile().course
            variables['course'] = course
            relevant_exams = Exam.objects.filter(course=course)
            relevant_exam_results = []
            for exam in relevant_exams:
                relevant_exam_results.extend(ExamResult.objects.filter(exam=exam, student=request.user))
            variables['exams'] = relevant_exam_results
        except Exception as e:
            pass
        return render(request, 'account/view-account.html', variables)

    else:
        if request.method == 'POST':
            form = LogInForm(request.POST)
            if form.is_valid():
                formemail = form.cleaned_data['email']
                password = form.cleaned_data['password']
                return log_user_in(request, formemail, password)
            else:
                print "Got invalid data."
        else:
            form = LogInForm()

        return render(request, 'account/log_in.html', 
                      { 'form' : form })

def log_user_in(request, formemail, password):
    user = authenticate(username=formemail, password=password)
    if user is None:
        print "Couldn't log you in."
        error = "Account name isn't in the database."
        if User.objects.filter(username=formemail).exists():
            error = "Account checks out, but that's the wrong password."
            form = LogInForm() # resets 'form'
            return render(request,
                          'account/log_in.html', {
                    'importantMessage' : error,
                    'form' : form,
                    })                          
        else:
            form = LogInForm() # resets 'form'
            return render(request,
                          'account/log_in.html', {
                    'importantMessage' : error,
                    'form' : form,
                    })
    else:
        login(request, user)
        return render(request,
                      'account/view-account.html', {
                'user' : request.user,
                'importantMessage' : 'You are logged in',
                'course' : request.user.get_profile().course,
                })


def create(request):
    if request.method == 'POST': # form was submitted
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            formemail = form.cleaned_data['email']
            password = form.cleaned_data['password']
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            cu_id = form.cleaned_data['cu_id']
            course = form.cleaned_data['course']
            print "Make account for %s %s <%s> (password hidden)" % (
                firstName, lastName, formemail)
            # first check to see if the user exists
            if User.objects.filter(username=formemail).exists():
                Errors = form._errors.setdefault("email", ErrorList())
                errors.append("Not unique. Please choose another.")
            else:
                newUser = User.objects.create_user(
                    formemail, email=formemail, password=password)
                newUser.first_name = firstName
                newUser.last_name = lastName
                newUser.save()
                retroUser = RetroUser()
                retroUser.user = newUser
                retroUser.course = course
                retroUser.cu_id = cu_id
                retroUser.save()
                #return HttpResponseRedirect("/account/thanks")
                return log_user_in(request, formemail, password)
    else:
        form = CreateAccountForm() # unbound, clean form

    return render(request, 'account/create.html',
                  { 'form' : form, })


def log_out(request):
    logout(request)
    return HttpResponseRedirect("/account/")

@login_required
def lookup(request):
    variables = {'user' : request.user }
    if request.user.is_authenticated() and request.user.is_staff:
        if request.method == 'POST':
            form = LookupForm(request.POST)
            variables['form'] = form
            if form.is_valid():
                # form valid
                first = form.cleaned_data['first']
                last = form.cleaned_data['last']
                sid =  form.cleaned_data['sid']
                all_data = [first, last, sid]
                users = get_all_user_matches(first, last, sid)
                variables['users'] = users
            else:
                # form invalid. try again.
                pass
        else:
            # create and send back form
            form = LookupForm()
            variables['form'] = form
    return render(request, 'account/lookup.html', variables)

def get_all_user_matches(first, last, sid):
    users = []
    valid_results = [] # list of lists
    first_results = None
    last_results = None
    sid_results = None
    if first is not None and len(first) > 0:
        first_results = User.objects.filter(first_name__iexact=first)
        valid_results.append(first_results)
        users.extend(first_results)
    if last is not None and len(last) > 0:
        last_results = User.objects.filter(last_name__iexact=last)
        valid_results.append(last_results)
        users.extend(last_results)
    if sid is not None and len(sid) > 0:
        retro_users = RetroUser.objects.filter(cu_id__iexact=sid)
        sid_results = []
        for ru in retro_users:
            users.append(ru.user)
            sid_results.append(ru.user)
        valid_results.append(sid_results)
    
    # see if there are matches to all of the input
    union = set()
    if (len(valid_results) > 0):
        union = set(valid_results[0])
        for i in range(len(valid_results) - 1):
            union = union & set(valid_results[i+1])
    if len(union) > 0:
        return union
    else:
        return set(users)

def intersect(a, b):
    return list(set(a) & set(b))
