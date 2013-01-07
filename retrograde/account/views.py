#
# views.py    - account
#

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from homework.models import Homework
from account.forms import CreateAccountForm

def index(request):
    if request.user.is_authenticated():
        return render_to_response('account/index.html', { 'user' : request.user } )
    else:
        return render_to_response('account/log_in.html' )


def create(request):
    if request.method == 'POST': # form was submitted
        pass
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            print "Make account for %s %s <%s> (%s)" % (firstName, lastName, email, password)

            return HttpResponseRedirect("/account/")

    else:
        form = CreateAccountForm() # unbound, clean form

    return render(request, 'account/create.html',
                  { 'form' : form, })

