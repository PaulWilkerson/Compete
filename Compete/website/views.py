from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden

def index(request):
    return render(request, 'index.html', {  } )
    