from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import subprocess
import sys
import traceback
import tempfile
import os
from .models import Week, Challenge, Submission, UserProgress
from .forms import WeekForm, ChallengeForm

@login_required
def week_challenges(request, week_number):
    week = get_object_or_404(Week, week_number=week_number)
    challenges = week.challenges.all().order_by('order')
    
    # Get user's progress for this week
    user_progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        week=week
    )
    if created:
        user_progress.total_challenges = challenges.count()
        user_progress.save()
    
    # Get user's submissions for these challenges
    user_submissions = {}
    if not request.user.is_superuser:
        submissions = Submission.objects.filter(
            user=request.user,
            challenge__in=challenges
        ).select_related('challenge')
        user_submissions = {sub.challenge.id: sub for sub in submissions}
    
    context = {
        'week': week,
        'challenges': challenges,
        'user_progress': user_progress,
        'user_submissions': user_submissions,
    }
    
    return render(request, 'challenges/week_challenges.html', context)

@login_required
def challenge_detail(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    
    # Get user's submission if exists
    user_submission = None
    if not request.user.is_superuser:
        try:
            user_submission = Submission.objects.get(
                user=request.user,
                challenge=challenge
            )
        except Submission.DoesNotExist:
            pass
    
    context = {
        'challenge': challenge,
        'user_submission': user_submission,
    }
    
    return render(request, 'challenges/challenge_detail.html', context)

@login_required
@require_POST
def submit_solution(request, challenge_id):
    if request.user.is_superuser:
        return JsonResponse({'error': 'Admins cannot submit solutions'}, status=403)
    
    challenge = get_object_or_404(Challenge, id=challenge_id)
    
    try:
        data = json.loads(request.body)
        submitted_code = data.get('code', '').strip()
        
        if not submitted_code:
            return JsonResponse({'error': 'Code cannot be empty'}, status=400)
        
        # Execute the code and get output
        execution_result = execute_python_code(submitted_code)
        
        # Check if output matches expected output
        status = 'correct' if execution_result['output'].strip() == challenge.expected_output.strip() else 'incorrect'
        points_earned = challenge.points if status == 'correct' else 0
        
        # Update or create submission
        submission, created = Submission.objects.update_or_create(
            user=request.user,
            challenge=challenge,
            defaults={
                'submitted_code': submitted_code,
                'output': execution_result['output'],
                'status': status,
                'points_earned': points_earned,
            }
        )
        
        # Update user progress
        user_progress, _ = UserProgress.objects.get_or_create(
            user=request.user,
            week=challenge.week
        )
        user_progress.update_progress()
        
        # Update user total score
        if created and status == 'correct':
            request.user.total_score += points_earned
            request.user.save()
        elif not created and status == 'correct' and submission.points_earned != points_earned:
            # Handle case where challenge points changed
            request.user.total_score += (points_earned - submission.points_earned)
            request.user.save()
        
        return JsonResponse({
            'status': status,
            'output': execution_result['output'],
            'points_earned': points_earned,
            'error': execution_result.get('error', ''),
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def execute_code(request):
    """Execute Python code and return output"""
    try:
        data = json.loads(request.body)
        code = data.get('code', '').strip()
        
        if not code:
            return JsonResponse({'error': 'Code cannot be empty'}, status=400)
        
        result = execute_python_code(code)
        return JsonResponse(result)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def execute_python_code(code):
    """Safely execute Python code and return output"""
    try:
        # Create a temporary file to write the code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # Execute the code using subprocess for security
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=10,  # 10 second timeout
                cwd=tempfile.gettempdir()
            )
            
            if result.returncode == 0:
                return {
                    'output': result.stdout,
                    'error': result.stderr if result.stderr else None
                }
            else:
                return {
                    'output': result.stdout,
                    'error': result.stderr or 'Code execution failed'
                }
                
        finally:
            # Clean up the temporary file
            os.unlink(temp_file)
            
    except subprocess.TimeoutExpired:
        return {
            'output': '',
            'error': 'Code execution timed out (10 seconds limit)'
        }
    except Exception as e:
        return {
            'output': '',
            'error': f'Execution error: {str(e)}'
        }

# Admin views
@login_required
@staff_member_required
def create_week(request):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:user_dashboard')
    
    if request.method == 'POST':
        form = WeekForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Week created successfully!')
            return redirect('dashboard:admin_dashboard')
    else:
        form = WeekForm()
    
    return render(request, 'challenges/create_week.html', {'form': form})

@login_required
@staff_member_required
def create_challenge(request):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:user_dashboard')
    
    if request.method == 'POST':
        form = ChallengeForm(request.POST)
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.created_by = request.user
            challenge.save()
            messages.success(request, 'Challenge created successfully!')
            return redirect('challenges:manage_challenges', week_id=challenge.week.id)
    else:
        form = ChallengeForm()
    
    return render(request, 'challenges/create_challenge.html', {'form': form})

@login_required
@staff_member_required
def manage_challenges(request, week_id):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:user_dashboard')
    
    week = get_object_or_404(Week, id=week_id)
    challenges = week.challenges.all().order_by('order')
    
    context = {
        'week': week,
        'challenges': challenges,
    }
    
    return render(request, 'challenges/manage_challenges.html', context)
