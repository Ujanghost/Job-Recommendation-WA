from django.db import models

class Preferences(models.Model):
    desired_roles = models.JSONField()
    locations = models.JSONField()
    job_type = models.CharField(max_length=50)

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    skills = models.JSONField()
    experience_level = models.CharField(max_length=50)
    preferences = models.OneToOneField(Preferences, on_delete=models.CASCADE)

class JobPosting(models.Model):
    job_id = models.IntegerField(unique=True)
    job_title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    required_skills = models.JSONField()
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50)
    experience_level = models.CharField(max_length=50)

# job_recommendation/forms.py
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
