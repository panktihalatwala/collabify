from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import User

def landing(request):
    from influencers.models import InfluencerProfile
    from campaigns.models import Campaign
    influencers = InfluencerProfile.objects.select_related('user').order_by('-followers_count')[:6]
    campaigns = Campaign.objects.filter(status='open').order_by('-created_at')[:3]
    return render(request, 'landing.html', {
        'influencers': influencers,
        'campaigns': campaigns,
    })

def role_select(request):
    return render(request, 'accounts/role_select.html')

def register(request):
    role = request.GET.get('role', 'influencer')
    if role not in ['influencer', 'brand']:
        role = 'influencer'

    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        role = request.POST.get('role', 'influencer')
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = role
            user.save()
            login(request, user)
            messages.success(request, f'Welcome to Collabify, {user.first_name or user.username}!')
            if user.role == 'influencer':
                return redirect('influencers:create_profile')
            else:
                return redirect('brands:create_profile')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = RegisterForm(initial={'role': role})

    return render(request, 'accounts/register.html', {'form': form, 'role': role})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('landing')