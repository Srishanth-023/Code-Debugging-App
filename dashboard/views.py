from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Count, Sum
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from datetime import date, timedelta
from challenges.models import Week, Challenge, Submission, UserProgress
from authentication.models import CustomUser

@login_required
def user_dashboard(request):
    if request.user.is_superuser:
        return redirect('dashboard:admin_dashboard')
    
    # Get current week
    today = date.today()
    current_week = Week.objects.filter(
        start_date__lte=today,
        end_date__gte=today
    ).first()
    
    # Get user's progress for current week
    user_progress = None
    if current_week:
        user_progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            week=current_week
        )
        if created:
            user_progress.total_challenges = current_week.challenges.count()
            user_progress.save()
        user_progress.update_progress()
    
    # Get recent submissions
    recent_submissions = Submission.objects.filter(
        user=request.user
    ).select_related('challenge', 'challenge__week')[:5]
    
    # Get all weeks for navigation
    all_weeks = Week.objects.all().order_by('-week_number')
    
    context = {
        'current_week': current_week,
        'user_progress': user_progress,
        'recent_submissions': recent_submissions,
        'all_weeks': all_weeks,
        'total_score': request.user.total_score,
    }
    
    return render(request, 'dashboard/user_dashboard.html', context)

@login_required
@staff_member_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard:user_dashboard')
    
    # Statistics
    total_users = CustomUser.objects.filter(user_type='user').count()
    total_weeks = Week.objects.count()
    total_challenges = Challenge.objects.count()
    total_submissions = Submission.objects.count()
    
    # Recent activity
    recent_submissions = Submission.objects.select_related(
        'user', 'challenge', 'challenge__week'
    ).order_by('-submitted_at')[:10]
    
    # Weekly statistics
    weekly_stats = Week.objects.annotate(
        challenge_count=Count('challenges'),
        submission_count=Count('challenges__submission')
    ).order_by('-week_number')[:5]
    
    context = {
        'total_users': total_users,
        'total_weeks': total_weeks,
        'total_challenges': total_challenges,
        'total_submissions': total_submissions,
        'recent_submissions': recent_submissions,
        'weekly_stats': weekly_stats,
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)
