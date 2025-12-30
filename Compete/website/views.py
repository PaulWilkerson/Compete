from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db.models import Sum
from .forms import CompetitorSignup, UpdateProfile
from .models import Account, SolvedChallenge

def home(request):
    return render(request, 'home.html', {  } )


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
    recent_activity = solved_challenges.order_by('-solved_at')[:10]
    
    context = {
        'objects': objects,
        'total_challenges_solved': total_challenges_solved,
        'total_points': total_points,
        'recent_activity': recent_activity,
    }
    
    return render(request, 'profile.html', context)
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
            return redirect('profile')
        else:
            return render(request, 'update_profile.html', { 'form': form } )
    else:
        form = UpdateProfile(instance=profile)
        return render(request, 'update_profile.html', { 'form': form } )

def leaderboard(request):
    # Get all users with their total points
    users_with_points = []
    all_users = User.objects.all()
    
    for user in all_users:
        solved_challenges = SolvedChallenge.objects.filter(user=user)
        total_points = sum(challenge.points for challenge in solved_challenges)
        total_challenges = solved_challenges.count()
        
        if total_points > 0 or total_challenges > 0:  # Only include users who have solved at least one challenge
            users_with_points.append({
                'user': user,
                'total_points': total_points,
                'total_challenges': total_challenges,
            })
    
    # Sort by points (descending) and take top 100
    users_with_points.sort(key=lambda x: x['total_points'], reverse=True)
    top_100_users = users_with_points[:100]
    
    # Add rank to each user
    for i, user_data in enumerate(top_100_users):
        user_data['rank'] = i + 1
    
    # Find current user's rank if authenticated
    current_user_rank = None
    if request.user.is_authenticated:
        for i, user_data in enumerate(users_with_points):
            if user_data['user'] == request.user:
                current_user_rank = i + 1
                break
    
    context = {
        'top_users': top_100_users,
        'current_user_rank': current_user_rank,
    }
    
    return render(request, 'leaderboard.html', context)