#
# views.py    - account
#

from django.forms.util import ErrorList
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, render
from homework.models import Homework, Course
from account.forms import CreateAccountForm
from account.forms import LogInForm
from django.contrib.auth.models import User
from account.models import RetroUser
from django.contrib.auth import authenticate, login, logout

def index(request):
    if request.user.is_authenticated():
        return render(request, 
                      'account/view-account.html', 
                      { 'user' : request.user,
                        'course' : request.user.get_profile().course,
                        })
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
        else:
            form = LogInForm() # resets 'form'
            return render(request,
                          'account/log_in.html', {
                    'importantMessage' : error,
                    'form' : form,
                    })
    else:
        print "Got correct credentials."
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

