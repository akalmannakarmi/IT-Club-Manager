from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['userId', 'name', 'courseId', 'batchId', 'skills']