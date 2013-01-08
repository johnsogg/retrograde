#
# views.py:retrograde
# 
# This is a catch-all for retrograde views. If it doesn't belong
# nicely anywhere else, it can go here.

from django.http import HttpResponseRedirect

def home(request):
    return HttpResponseRedirect("/account")
    
