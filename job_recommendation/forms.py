from django import forms
from .models import UserProfile, Preferences, JobPosting

class PreferencesForm(forms.ModelForm):
    class Meta:
        model = Preferences
        fields = ['desired_roles', 'locations', 'job_type']
        widgets = {
            'desired_roles': forms.TextInput(attrs={'placeholder': 'Enter desired roles separated by commas'}),
            'locations': forms.TextInput(attrs={'placeholder': 'Enter locations separated by commas'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'skills', 'experience_level']
        widgets = {
            'skills': forms.TextInput(attrs={'placeholder': 'Enter skills separated by commas'}),
        }

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['job_id', 'job_title', 'company', 'required_skills', 'location', 'job_type', 'experience_level']
        widgets = {
            'required_skills': forms.TextInput(attrs={'placeholder': 'Enter required skills separated by commas'}),
        }
        