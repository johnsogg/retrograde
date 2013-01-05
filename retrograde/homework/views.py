#
# views.py    - homework
#

"""
This is a test.
"""

from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from homework.models import Homework

def index(request):
    """
    Word! Now I can document things and have it show up on some admin
    documentation thing. Zany.
    """

    greeting = "This is a fantastic greeting for Sputnik"
    return render_to_response("homework/index.html", {"greeting" : greeting})

def specific(request, hw_id):
    p = get_object_or_404(Homework, pk=hw_id)
    return render_to_response('homework/detail.html', {'homework': p})
