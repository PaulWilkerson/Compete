from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .forms import CompetitorSignup, UpdateProfile
from .models import Account, SolvedChallenge

def home(request):
    return render(request, 'home.html', {  } )

def documentation(request):
    return render(request, 'documentation.html', {  } )
@csrf_protect
def signup(request):
    if request.method == 'POST':
        form = CompetitorSignup(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after successful signup
            login(request, user)
            # Create an Account profile for the user
            Account.objects.create(user=user, firstname='', lastname='', about='', website='')
            return redirect('home')
    else:
        form = CompetitorSignup()
    return render(request, 'signup.html', {'form': form})
@login_required
def logout_view(request):
    logout(request)
    return render(request, 'logout.html', {  } )
@login_required
def profile(request):
    objects = Account.objects.filter(user=request.user)
    
    # Calculate user stats
    solved_challenges = SolvedChallenge.objects.filter(user=request.user)
    total_challenges_solved = solved_challenges.count()
    total_points = sum(challenge.points for challenge in solved_challenges)
    
    # Get recent activity
    recent_activity = solved_challenges[:10]
    
    context = {
        'objects': objects,
        'total_challenges_solved': total_challenges_solved,
        'total_points': total_points,
        'recent_activity': recent_activity,
    }
    
    return render(request, 'account/profile.html', context)
@login_required
def update_profile(request):
    try:
        profile = Account.objects.get(user=request.user)
    except Account.DoesNotExist:
        profile = Account(user=request.user)
        profile.save()
    
    if request.method == 'POST':
        form = UpdateProfile(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return render(request, 'account/profile.html', { 'objects': [profile] } )
        else:
            return render(request, 'account/update_profile.html', { 'form': form } )
    else:
        form = UpdateProfile(instance=profile)
        return render(request, 'account/update_profile.html', { 'form': form } )