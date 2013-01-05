#
# views.py    - account
#

from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from homework.models import Homework

def index(request):
    if request.user.is_authenticated():
        return render_to_response('account/index.html', { 'user' : request.user } )
    else:
        return render_to_response('account/log_in.html' )

