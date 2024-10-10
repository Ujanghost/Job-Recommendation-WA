from django.test import TestCase, Client
from django.urls import reverse
from django.http import JsonResponse
from unittest.mock import patch
from .models import UserProfile, Preferences, JobPosting
from .forms import UserProfileForm, PreferencesForm, JobPostingForm

class JobRecommendationTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user_profile = UserProfile.objects.create(name="John Doe", skills="Python", experience_level="Intermediate")
        self.preferences = Preferences.objects.create(desired_roles="Developer", locations="Remote", job_type="Full-time")
        self.job_posting = JobPosting.objects.create(job_id=1, job_title="Software Engineer", company="Tech Inc.", required_skills="Python, Django", location="Remote", job_type="Full-time", experience_level="Intermediate")
    
    # Test home view
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_recommendation/home.html')

    # Test create user profile
    @patch('requests.post')
    def test_create_user_profile_view_post(self, mock_post):
        mock_post.return_value.status_code = 200
        response = self.client.post(reverse('create_user_profile'), {
            'name': 'John Doe',
            'skills': 'Python, Django',
            'experience_level': 'Intermediate',
            'desired_roles': 'Developer',
            'locations': 'Remote',
            'job_type': 'Full-time',
        })
        self.assertEqual(response.status_code, 302)  # Redirect to job recommendations
        self.assertTrue(UserProfile.objects.filter(name='John Doe').exists())
    
    def test_create_user_profile_view_get(self):
        response = self.client.get(reverse('create_user_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_recommendation/create_user_profile.html')

    # Test job recommendations
    @patch('requests.get')
    def test_job_recommendations_view(self, mock_get):
        mock_get.return_value = JsonResponse([{'job_title': 'Software Engineer', 'company': 'Tech Inc.'}], safe=False)
        response = self.client.get(reverse('job_recommendations', args=[self.user_profile.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_recommendation/job_recommendations.html')

    # Test all job postings view
    @patch('requests.get')
    def test_all_job_postings_view(self, mock_get):
        mock_get.return_value = JsonResponse([{'job_title': 'Software Engineer', 'company': 'Tech Inc.'}], safe=False)
        response = self.client.get(reverse('all_job_postings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_recommendation/all_job_postings.html')

    # Test create job posting
    @patch('requests.post')
    def test_create_job_posting_view_post(self, mock_post):
        mock_post.return_value.status_code = 200
        response = self.client.post(reverse('create_job_posting'), {
            'job_title': 'Backend Developer',
            'company': 'Tech Inc.',
            'required_skills': 'Python, Django',
            'location': 'Remote',
            'job_type': 'Full-time',
            'experience_level': 'Senior',
        })
        self.assertEqual(response.status_code, 302)  # Redirect to all job postings
        self.assertTrue(JobPosting.objects.filter(job_title='Backend Developer').exists())
    
    def test_create_job_posting_view_get(self):
        response = self.client.get(reverse('create_job_posting'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_recommendation/create_job_posting.html')

    # Test update job posting
    @patch('requests.put')
    def test_update_job_posting_view_post(self, mock_put):
        mock_put.return_value.status_code = 200
        response = self.client.post(reverse('update_job_posting', args=[self.job_posting.job_id]), {
            'job_title': 'Updated Job Title',
            'company': 'Tech Corp',
            'required_skills': 'Python, Django, Flask',
            'location': 'On-site',
            'job_type': 'Part-time',
            'experience_level': 'Intermediate',
        })
        self.assertEqual(response.status_code, 302)  # Redirect to all job postings
        updated_job_posting = JobPosting.objects.get(job_id=self.job_posting.job_id)
        self.assertEqual(updated_job_posting.job_title, 'Updated Job Title')

    def test_update_job_posting_view_get(self):
        response = self.client.get(reverse('update_job_posting', args=[self.job_posting.job_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_recommendation/update_job_posting.html')

    # Test delete job posting
    @patch('requests.delete')
    def test_delete_job_posting_view_post(self, mock_delete):
        mock_delete.return_value.status_code = 200
        response = self.client.post(reverse('delete_job_posting', args=[self.job_posting.job_id]))
        self.assertEqual(response.status_code, 302)  # Redirect to all job postings
        self.assertFalse(JobPosting.objects.filter(job_id=self.job_posting.job_id).exists())

    def test_delete_job_posting_view_get(self):
        response = self.client.get(reverse('delete_job_posting', args=[self.job_posting.job_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job_recommendation/delete_job_posting.html')
