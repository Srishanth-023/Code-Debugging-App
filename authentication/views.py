from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import RegistrationForm, LoginForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:user_dashboard')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('authentication:login')
    else:
        form = RegistrationForm()
    
    return render(request, 'authentication/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_admin_user:
            return redirect('dashboard:admin_dashboard')
        else:
            return redirect('dashboard:user_dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            
            # Redirect based on user type
            if user.is_admin_user:
                return redirect('dashboard:admin_dashboard')
            else:
                return redirect('dashboard:user_dashboard')
    else:
        form = LoginForm()
    
    return render(request, 'authentication/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('authentication:login')
