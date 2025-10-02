from django.urls import path
from . import views

app_name = 'challenges'

urlpatterns = [
    path('week/<int:week_number>/', views.week_challenges, name='week_challenges'),
    path('challenge/<int:challenge_id>/', views.challenge_detail, name='challenge_detail'),
    path('submit/<int:challenge_id>/', views.submit_solution, name='submit_solution'),
    path('execute/', views.execute_code, name='execute_code'),
    
    # Admin URLs
    path('admin/create-week/', views.create_week, name='create_week'),
    path('admin/create-challenge/', views.create_challenge, name='create_challenge'),
    path('admin/week/<int:week_id>/challenges/', views.manage_challenges, name='manage_challenges'),
]