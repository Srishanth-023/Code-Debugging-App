from django.db import models
from django.conf import settings
from datetime import date, timedelta

class Week(models.Model):
    week_number = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-week_number']
    
    def __str__(self):
        return f"Week {self.week_number}: {self.title}"
    
    @property
    def is_current_week(self):
        today = date.today()
        return self.start_date <= today <= self.end_date
    
    @property
    def is_past_week(self):
        return date.today() > self.end_date
    
    @property
    def is_future_week(self):
        return date.today() < self.start_date

class Challenge(models.Model):
    DIFFICULTY_CHOICES = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )
    
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name='challenges')
    title = models.CharField(max_length=200)
    description = models.TextField()
    buggy_code = models.TextField()
    expected_output = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    points = models.IntegerField(default=1)
    order = models.IntegerField(default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['week', 'order']
        unique_together = ['week', 'order']
    
    def __str__(self):
        return f"{self.week} - {self.title}"

class Submission(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('correct', 'Correct'),
        ('incorrect', 'Incorrect'),
        ('error', 'Error'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    submitted_code = models.TextField()
    output = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    points_earned = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-submitted_at']
        unique_together = ['user', 'challenge']
    
    def __str__(self):
        return f"{self.user.username} - {self.challenge.title} ({self.status})"

class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    challenges_completed = models.IntegerField(default=0)
    total_challenges = models.IntegerField(default=0)
    points_earned = models.IntegerField(default=0)
    completion_percentage = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'week']
    
    def __str__(self):
        return f"{self.user.username} - {self.week}"
    
    def update_progress(self):
        """Update progress based on submissions"""
        completed_submissions = Submission.objects.filter(
            user=self.user,
            challenge__week=self.week,
            status='correct'
        ).count()
        
        total_challenges = self.week.challenges.count()
        earned_points = Submission.objects.filter(
            user=self.user,
            challenge__week=self.week,
            status='correct'
        ).aggregate(total=models.Sum('points_earned'))['total'] or 0
        
        self.challenges_completed = completed_submissions
        self.total_challenges = total_challenges
        self.points_earned = earned_points
        self.completion_percentage = (completed_submissions / total_challenges * 100) if total_challenges > 0 else 0
        self.save()
