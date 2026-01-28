from django import forms
from django.contrib.auth.models import User
from .models import Profile

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    username = forms.CharField(
        max_length=150,
        required=True,
        help_text=''
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class TeacherRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    employee_id = forms.CharField(max_length=20)

    username = forms.CharField(
        max_length=150,
        required=True,
        help_text=''
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['attendance', 'last_semester_marks', 'grade']
