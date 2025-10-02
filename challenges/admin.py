from django.contrib import admin
from .models import Week, Challenge, Submission, UserProgress

@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):
    list_display = ['week_number', 'title', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active', 'start_date']
    search_fields = ['title', 'description']
    ordering = ['-week_number']

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['title', 'week', 'difficulty', 'points', 'order', 'created_by']
    list_filter = ['week', 'difficulty', 'created_by']
    search_fields = ['title', 'description']
    ordering = ['week', 'order']

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'challenge', 'status', 'points_earned', 'submitted_at']
    list_filter = ['status', 'challenge__week', 'submitted_at']
    search_fields = ['user__username', 'challenge__title']
    readonly_fields = ['submitted_at']
    ordering = ['-submitted_at']

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'week', 'challenges_completed', 'total_challenges', 'points_earned', 'completion_percentage']
    list_filter = ['week', 'last_updated']
    search_fields = ['user__username']
    readonly_fields = ['last_updated']
