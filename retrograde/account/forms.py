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
    courses = Course.objects.all()
    course = forms.ModelChoiceField(queryset=courses, empty_label=None)

class LogInForm(forms.Form):
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),
                               label="Password")
