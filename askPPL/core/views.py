from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def profile(request):
    return render(request, 'core/profile.html')

def login(request):
    return render(request, 'core/login.html')

def signup(request):
    return render(request, 'core/signup.html')