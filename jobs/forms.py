from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Application, Message

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

# Registration forms for students and employers.
class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class EmployerRegistrationForm(UserCreationForm):
    company_name = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'company_name']
