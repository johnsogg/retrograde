# Create your views here.

#from django.http import HttpResponse
#from django.template import Context, loader
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from homework.models import Homework

def index(request):
    greeting = "This is a fantastic greeting for Sputnik"
    return render_to_response("homework/index.html", {"greeting" : greeting})

def specific(request, hw_id):
    p = get_object_or_404(Homework, pk=hw_id)
    return render_to_response('homework/detail.html', {'homework': p})
