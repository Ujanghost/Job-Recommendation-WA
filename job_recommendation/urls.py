from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Add this line for the home page
    path('create_profile/', views.create_user_profile, name='create_user_profile'),
    path('recommendations/<int:user_id>/', views.job_recommendations, name='job_recommendations'),
    path('job_postings/', views.all_job_postings, name='all_job_postings'),
    path('create_job_posting/', views.create_job_posting, name='create_job_posting'),
    path('update_job_posting/<int:job_id>/', views.update_job_posting, name='update_job_posting'),
    path('delete_job_posting/<int:job_id>/', views.delete_job_posting, name='delete_job_posting'),
    path('create_profile/', views.create_user_profile, name='create_user_profile'),
    path('job_postings/', views.all_job_postings, name='all_job_postings'),
    path('create_job_posting/', views.create_job_posting, name='create_job_posting'),

]