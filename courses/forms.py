from django import forms
from .models import Enrollment,Forum

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['completed']

class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['message']

