from django import forms
from homework.models import Course

class CreateAccountForm(forms.Form):
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),
                               label="Password")
    firstName = forms.CharField(required=False,
                                label="First Name")
    lastName = forms.CharField(required=False,
                               label="Last Name")
    cu_id = forms.CharField(required=True,
                            label="CU Student ID")
    courses = Course.objects.all()
    course = forms.ModelChoiceField(queryset=courses, required=True, empty_label="Choose A Course")

class LogInForm(forms.Form):
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),
                               label="Password")
