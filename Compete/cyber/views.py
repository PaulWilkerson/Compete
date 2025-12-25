from django.shortcuts import render, get_object_or_404, redirect
from .models import NewCyberChallenge
from .forms import ChallengeForm
from django.http import HttpResponse

def challenge_list(request):
    challenges = NewCyberChallenge.objects.all()
    return render(request, 'cyber/challenge_list.html', {'challenges': challenges})
def challenge_detail(request, challenge_id):
    challenge = get_object_or_404(NewCyberChallenge, id=challenge_id)
    return render(request, 'cyber/challenge_detail.html', {'challenge': challenge})
def new_challenge(request):
    if request.method == 'POST':
        form = ChallengeForm(request.POST)
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.flag = request.POST.get('flag', '')
            challenge.save()
            return redirect('cyber_challenge_list')
    else:
        form = ChallengeForm()
    return render(request, 'cyber/new_challenge.html', {'form': form})