from django import forms
from homework.models import *

class GradeExamForm(forms.Form):
    firstName = forms.CharField(required=False,
                                label="First Name")
    lastName = forms.CharField(required=False,
                               label="Last Name")
    cu_id = forms.CharField(required=True,
                            label="CU Student ID")
    score = forms.IntegerField(required=True,
                               label="Score")
    tas = TeachingAssistant.objects.all()
    ta = forms.ModelChoiceField(queryset=tas, required=False, empty_label="Unknown TA", label="Teaching Assistant") 
    courses = Course.objects.all()
    course = forms.ModelChoiceField(queryset=courses, required=True, empty_label="Choose A Course")
