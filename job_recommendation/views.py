from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from .models import UserProfile, JobPosting
from .forms import UserProfileForm, PreferencesForm, JobPostingForm
import requests


API_BASE_URL = 'http://localhost:8000'

def home(request):
    return render(request, 'job_recommendation/home.html')
def create_user_profile(request):
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST)
        preferences_form = PreferencesForm(request.POST)
        if user_form.is_valid() and preferences_form.is_valid():
            preferences = preferences_form.save()
            user_profile = user_form.save(commit=False)
            user_profile.preferences = preferences
            user_profile.save()
            
            data = {
                'name': user_profile.name,
                'skills': user_profile.skills,
                'experience_level': user_profile.experience_level,
                'preferences': {
                    'desired_roles': preferences.desired_roles,
                    'locations': preferences.locations,
                    'job_type': preferences.job_type,
                }
            }
            response = requests.post(f'{API_BASE_URL}/user_profile', json=data)
            if response.status_code == 200:
                return redirect('job_recommendations', user_id=user_profile.id)
    else:
        user_form = UserProfileForm()
        preferences_form = PreferencesForm()
    return render(request, 'job_recommendation/create_user_profile.html', {'user_form': user_form, 'preferences_form': preferences_form})

def job_recommendations(request, user_id):
    user_profile = get_object_or_404(UserProfile, id=user_id)
    response = requests.get(f'{API_BASE_URL}/job_recommendations/{user_id}')
    if response.status_code == 200:
        jobs = response.json()
        return render(request, 'job_recommendation/job_recommendations.html', {'jobs': jobs, 'user_profile': user_profile})
    else:
        return render(request, 'job_recommendation/error.html', {'message': 'Failed to fetch job recommendations'})

def all_job_postings(request):
    response = requests.get(f'{API_BASE_URL}/job_postings')
    if response.status_code == 200:
        jobs = response.json()
        return render(request, 'job_recommendation/all_job_postings.html', {'jobs': jobs})
    else:
        return render(request, 'job_recommendation/error.html', {'message': 'Failed to fetch job postings'})

def create_job_posting(request):
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job_posting = form.save(commit=False)
            data = {
                'job_id': job_posting.job_id,
                'job_title': job_posting.job_title,
                'company': job_posting.company,
                'required_skills': job_posting.required_skills,
                'location': job_posting.location,
                'job_type': job_posting.job_type,
                'experience_level': job_posting.experience_level,
            }
            response = requests.post(f'{API_BASE_URL}/job_posting', json=data)
            if response.status_code == 200:
                job_posting.save()
                return redirect('all_job_postings')
            else:
                return render(request, 'job_recommendation/error.html', {'message': 'Failed to create job posting'})
    else:
        form = JobPostingForm()
    return render(request, 'job_recommendation/create_job_posting.html', {'form': form})

def update_job_posting(request, job_id):
    job_posting = get_object_or_404(JobPosting, job_id=job_id)
    if request.method == 'POST':
        form = JobPostingForm(request.POST, instance=job_posting)
        if form.is_valid():
            updated_job = form.save(commit=False)
            data = {
                'job_id': updated_job.job_id,
                'job_title': updated_job.job_title,
                'company': updated_job.company,
                'required_skills': updated_job.required_skills,
                'location': updated_job.location,
                'job_type': updated_job.job_type,
                'experience_level': updated_job.experience_level,
            }
            response = requests.put(f'{API_BASE_URL}/job_posting/{job_id}', json=data)
            if response.status_code == 200:
                updated_job.save()
                return redirect('all_job_postings')
            else:
                return render(request, 'job_recommendation/error.html', {'message': 'Failed to update job posting'})
    else:
        form = JobPostingForm(instance=job_posting)
    return render(request, 'job_recommendation/update_job_posting.html', {'form': form, 'job_id': job_id})

def delete_job_posting(request, job_id):
    job_posting = get_object_or_404(JobPosting, job_id=job_id)
    if request.method == 'POST':
        response = requests.delete(f'{API_BASE_URL}/job_posting/{job_id}')
        if response.status_code == 200:
            job_posting.delete()
            return redirect('all_job_postings')
        else:
            return render(request, 'job_recommendation/error.html', {'message': 'Failed to delete job posting'})
    return render(request, 'job_recommendation/delete_job_posting.html', {'job': job_posting})

# job_recommendation/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create_profile/', views.create_user_profile, name='create_user_profile'),
    path('recommendations/<int:user_id>/', views.job_recommendations, name='job_recommendations'),
    path('job_postings/', views.all_job_postings, name='all_job_postings'),
    path('create_job_posting/', views.create_job_posting, name='create_job_posting'),
    path('update_job_posting/<int:job_id>/', views.update_job_posting, name='update_job_posting'),
    path('delete_job_posting/<int:job_id>/', views.delete_job_posting, name='delete_job_posting'),
]
