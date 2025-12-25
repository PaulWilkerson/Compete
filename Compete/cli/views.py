from django.shortcuts import render, get_object_or_404, redirect
from .models import NewCLIChallenge
from .forms import CLIChallengeForm
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from website.models import SolvedChallenge
from django.views.decorators.http import require_POST

@login_required
def challenge_list(request):
    challenges = NewCLIChallenge.objects.all()
    total_challenges = challenges.count()
    
    # Count solved challenges for current user
    solved_count = SolvedChallenge.objects.filter(
        user=request.user,
        challenge_type='cli'
    ).count()
    
    remaining_count = total_challenges - solved_count
    
    return render(request, 'cli/challenge_list.html', {
        'challenges': challenges,
        'total_challenges': total_challenges,
        'solved_count': solved_count,
        'remaining_count': remaining_count
    })

def challenge_detail(request, challenge_id):
    challenge = get_object_or_404(NewCLIChallenge, id=challenge_id)
    
    # Calculate total solves for this challenge
    total_solves = SolvedChallenge.objects.filter(
        challenge_type='cli',
        challenge_id=challenge_id
    ).count()
    
    # Check if already solved
    already_solved = False
    if request.user.is_authenticated:
        already_solved = SolvedChallenge.objects.filter(
            user=request.user,
            challenge_type='cli',
            challenge_id=challenge_id
        ).exists()
    
    # Handle flag submission
    if request.method == 'POST' and request.user.is_authenticated:
        submitted_flag = request.POST.get('flag', '').strip()
        
        if submitted_flag == challenge.flag:
            # Award points if not already solved
            if not already_solved:
                points = 100  # Default points for all challenges
                SolvedChallenge.objects.create(
                    user=request.user,
                    challenge_type='cli',
                    challenge_id=challenge.id,
                    challenge_title=challenge.title,
                    points=points
                )
                return JsonResponse({
                    'success': True,
                    'message': f'Congratulations! You solved the challenge and earned {points} points!'
                })
            else:
                return JsonResponse({
                    'success': True,
                    'message': 'Correct flag! (Already solved)'
                })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Incorrect flag. Try again!'
            })
    
    return render(request, 'cli/challenge_detail.html', {
        'challenge': challenge,
        'already_solved': already_solved,
        'total_solves': total_solves
    })
def new_challenge(request):
    if request.method == 'POST':
        form = CLIChallengeForm(request.POST)
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.flag = request.POST.get('flag', '')
            challenge.save()
            return redirect('cli_challenge_list')
    else:
        form = CLIChallengeForm()
    return render(request, 'cli/new_challenge.html', {'form': form})