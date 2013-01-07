#
# views.py    - account
#

from django.forms.util import ErrorList
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from homework.models import Homework
from account.forms import CreateAccountForm
from account.forms import LogInForm
from django.contrib.auth.models import User
from account.models import RetroUser
from django.contrib.auth import authenticate, login, logout

def index(request):
    if request.user.is_authenticated():
        return render_to_response('account/view-account.html', { 'user' : request.user } )
    else:
        if request.method == 'POST':
            form = LogInForm(request.POST)
            if form.is_valid():
                formemail = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = authenticate(username=formemail, password=password)
                if user is None:
                    print "Couldn't log you in."
                else:
                    print "Got correct credentials."
                    login(request, user)
                    return render_to_response('account/view-account.html', {
                            'user' : request.user,
                            'importantMessage' : 'You are logged in',
                            })
            else:
                print "Got invalid data."
        else:
            form = LogInForm()

        return render(request, 'account/log_in.html', 
                      { 'form' : form })


def create(request):
    if request.method == 'POST': # form was submitted
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            formemail = form.cleaned_data['email']
            password = form.cleaned_data['password']
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            print "Make account for %s %s <%s> (password hidden)" % (
                firstName, lastName, formemail)
            # first check to see if the user exists
            if User.objects.filter(username=formemail).exists():
                errors = form._errors.setdefault("email", ErrorList())
                errors.append("Not unique. Please choose another.")
            else:
                newUser = User.objects.create_user(
                    formemail, email=formemail, password=password)
                retroUser = RetroUser()
                retroUser.user = newUser
                retroUser.firstName = firstName
                retroUser.lastName = lastName
                retroUser.save()
                return HttpResponseRedirect("/account/")

    else:
        form = CreateAccountForm() # unbound, clean form

    return render(request, 'account/create.html',
                  { 'form' : form, })


def log_out(request):
    logout(request)
    return HttpResponseRedirect("/account/")
