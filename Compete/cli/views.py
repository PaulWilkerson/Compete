from django.shortcuts import render, get_object_or_404, redirect
from .models import NewCLIChallenge
from .forms import CLIChallengeForm
from django.http import HttpResponse

def challenge_list(request):
    challenges = NewCLIChallenge.objects.all()
    return render(request, 'cli/challenge_list.html', {'challenges': challenges})
def challenge_detail(request, challenge_id):
    challenge = get_object_or_404(NewCLIChallenge, id=challenge_id)
    return render(request, 'cli/challenge_detail.html', {'challenge': challenge})
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