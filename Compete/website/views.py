from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db.models import Sum, Count
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
    # Get all users with their total points using aggregation
    users_with_points = User.objects.annotate(
        total_points=Sum('solved_challenges__points'),
        total_challenges=Count('solved_challenges')
    ).filter(
        total_points__gt=0
    ).order_by('-total_points', 'id')[:100]  # Secondary sort by id for deterministic ordering
    
    # Convert to list and add ranks
    top_100_users = []
    for i, user in enumerate(users_with_points):
        top_100_users.append({
            'user': user,
            'total_points': user.total_points or 0,
            'total_challenges': user.total_challenges,
            'rank': i + 1,
        })
    
    # Find current user's rank if authenticated
    current_user_rank = None
    if request.user.is_authenticated:
        user_with_rank = User.objects.annotate(
            total_points=Sum('solved_challenges__points')
        ).filter(
            total_points__gt=0
        ).order_by('-total_points', 'id')  # Secondary sort by id for deterministic ordering
        
        for i, user in enumerate(user_with_rank):
            if user == request.user:
                current_user_rank = i + 1
                break
    
    context = {
        'top_users': top_100_users,
        'current_user_rank': current_user_rank,
    }
    
    return render(request, 'leaderboard.html', context)