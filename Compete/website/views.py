from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .forms import CompetitorSignup, UpdateProfile
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
    return render(request, 'account/profile.html', { 'objects': objects } )
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