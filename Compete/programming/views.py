from django.shortcuts import render, get_object_or_404, redirect
from .models import NewProgrammingChallenge
from .forms import ChallengeForm
from .judge0_service import Judge0Service
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from website.models import SolvedChallenge
from django.views.decorators.http import require_POST
@login_required
def challenge_list(request):
    challenges = NewProgrammingChallenge.objects.all()
    difficulty = request.GET.get('difficulty')
    category = request.GET.get('category')
    search_query = request.GET.get('search')
    if difficulty:
        challenges = challenges.filter(difficulty=difficulty)
    if category:
        challenges = challenges.filter(category=category)
    if search_query:
        challenges = challenges.filter(name__icontains=search_query)
    total_challenges = challenges.count()
    solved_count = SolvedChallenge.objects.filter(
        user=request.user,
        challenge_type='programming'
    ).count()
    
    remaining_count = total_challenges - solved_count
    
    return render(request, 'programming/challenge_list.html', {
        'challenges': challenges,
        'total_challenges': total_challenges,
        'solved_count': solved_count,
        'remaining_count': remaining_count
    })
@login_required
def challenge_detail(request, challenge_id):
    challenge = get_object_or_404(NewProgrammingChallenge, id=challenge_id)
    
    # Calculate total solves for this challenge
    total_solves = SolvedChallenge.objects.filter(
        challenge_type='programming',
        challenge_id=challenge_id
    ).count()
    
    # Check if already solved
    already_solved = False
    if request.user.is_authenticated:
        already_solved = SolvedChallenge.objects.filter(
            user=request.user,
            challenge_type='programming',
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
                    challenge_type='programming',
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
    
    return render(request, 'programming/challenge_detail.html', {
        'challenge': challenge,
        'already_solved': already_solved,
        'total_solves': total_solves
    })

@login_required
@require_POST
def execute_code(request):
    """Execute code using self-hosted Judge0 API"""
    try:
        code = request.POST.get('code', '').strip()
        language = request.POST.get('language', 'Python')
        stdin = request.POST.get('stdin', '')
        
        if not code:
            return JsonResponse({
                'success': False,
                'error': 'Code cannot be empty'
            })
        
        # Execute code using Judge0
        judge0 = Judge0Service()
        result = judge0.execute_code(code, language, stdin)
        
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        })

def new_challenge(request):
    if request.method == 'POST':
        form = ChallengeForm(request.POST)
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.flag = request.POST.get('flag', '')
            challenge.save()
            return redirect('programming_challenge_list')
    else:
        form = ChallengeForm()
    return render(request, 'programming/new_challenge.html', {'form': form})
