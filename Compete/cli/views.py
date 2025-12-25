from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .forms import CompetitorSignup
from .models import Account

def home(request):
    return render(request, 'home.html', {  } )
@csrf_protect
def signup(request):
    form = CompetitorSignup()
    return render(request, 'signup.html', { 'form': form } )
@login_required
def logout_view(request):
    logout(request)
    return render(request, 'logout.html', {  } )
@login_required
def profile(request):
    objects = Account.objects.filter(user=request.user)
    return render(request, 'profile.html', { 'objects': objects } )
@login_required
def update_profile(request):
    if request.method == 'post':
        profile = objects.get(user=request.user)
        form = modelsUpdateProfile(request.POST, instance=profile)
    return render(request, 'update_profile.html', { 'form': form } )