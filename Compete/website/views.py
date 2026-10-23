from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db.models import Sum, Count, Max
from .forms import CompetitorSignup, UpdateProfile
from .models import Account, SolvedChallenge
def home(request):
    try:
        from marketplace.models import HostedCTF
        open_ctfs = (
            HostedCTF.objects.filter(status=HostedCTF.STATUS_OPEN)
            .select_related("owner")
            .order_by("-created_at")[:6]
        )
        return render(request, 'home.html', {"open_ctfs": open_ctfs})
    except Exception:
        return render(request, '404.html', {  } )
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
    try:
        logout(request)
        return render(request, 'logout.html', {  } )
    except:
        def page_not_found(request):
            return render(request, '404.html', {  } )
@login_required
def profile(request, username=None):
    try:
        # If username is provided, show that user's profile, otherwise show own profile
        if username:
            try:
                profile_user = User.objects.get(username=username)
            except User.DoesNotExist:
                return redirect('home')
        else:
            profile_user = request.user
    
        objects = Account.objects.filter(user=profile_user)
    
        # Calculate user stats
        solved_challenges = SolvedChallenge.objects.filter(user=profile_user)
        total_challenges_solved = solved_challenges.count()
        total_points = sum(challenge.points for challenge in solved_challenges)
    
        # Get recent activity
        recent_activity = solved_challenges.order_by('-solved_at')[:10]
    
        # Calculate user's rank
        user_rank = get_user_rank(profile_user)
    
        context = {
            'objects': objects,
            'profile_user': profile_user,
            'total_challenges_solved': total_challenges_solved,
            'total_points': total_points,
            'recent_activity': recent_activity,
            'user_rank': user_rank,
            'is_own_profile': profile_user == request.user,
         }
    
        return render(request, 'profile.html', context)
    except:
        def page_not_found(request):
            return render(request, '404.html', {  } )
@login_required
def update_profile(request):
    try:
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
    except:
        return render(request, '404.html', {  } )
def privacy_policy(request):
    try:
        return render(request, 'privacy_policy.html', {})
    except:
        return render(request, '404.html', {  } )
def terms_of_service(request):
    try:
        return render(request, 'terms_of_service.html', {  } )
    except:
        return render(request, '404.html', {  } )
def get_user_rank(user):
    """Calculate the rank of a user based on total points."""
    # Get user's total points
    user_points = SolvedChallenge.objects.filter(user=user).aggregate(
        total=Sum('points')
    )['total'] or 0
    
    # Get the earliest solve time for the user (for tie-breaking)
    user_earliest = SolvedChallenge.objects.filter(user=user).aggregate(
        earliest=Max('solved_at')
    )['earliest']
    
    # Calculate rank: count users with more points, or same points but earlier solve time
    users_with_scores = User.objects.annotate(
        total_points=Sum('solved_challenges__points'),
        earliest_solve=Max('solved_challenges__solved_at')
    ).filter(total_points__isnull=False)
    
    rank = 1
    for other_user in users_with_scores:
        if other_user.id == user.id:
            continue
        other_points = other_user.total_points or 0
        if other_points > user_points:
            rank += 1
        elif other_points == user_points and user_earliest:
            # Tie-breaker: earlier solve time gets better rank
            if other_user.earliest_solve and other_user.earliest_solve < user_earliest:
                rank += 1
     
    return rank if user_points > 0 else None

def leaderboard(request):
    try:
        """Display the top 100 users by points."""
        # Get all users with their total points and challenge counts
        users_with_scores = User.objects.annotate(
            total_points=Sum('solved_challenges__points'),
            challenges_solved=Count('solved_challenges', distinct=True),
            earliest_solve=Max('solved_challenges__solved_at')
        ).filter(total_points__isnull=False).order_by('-total_points', 'earliest_solve')[:100]
    
        # Create leaderboard entries with ranks
        leaderboard_data = []
        for idx, user in enumerate(users_with_scores, start=1):
            leaderboard_data.append({
                'rank': idx,
                'username': user.username,
                'total_points': user.total_points or 0,
                'challenges_solved': user.challenges_solved or 0,
            })
    
        # Get current user's stats if authenticated
        user_rank = None
        user_points = 0
        user_challenges_solved = 0
        if request.user.is_authenticated:
            user_rank = get_user_rank(request.user)
            user_stats = SolvedChallenge.objects.filter(user=request.user).aggregate(
                total=Sum('points'),
                count=Count('id')
            )
            user_points = user_stats['total'] or 0
            user_challenges_solved = user_stats['count'] or 0
    
        context = {
            'leaderboard': leaderboard_data,
            'user_rank': user_rank,
            'user_points': user_points,
            'user_challenges_solved': user_challenges_solved,
        }
    
        return render(request, 'leaderboard.html', context)
    except:
        return render(request, '404.html', {  } )
