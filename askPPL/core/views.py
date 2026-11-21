from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import CustomLoginForm, CustomSignupForm, CustomProfileForm
from django.http import HttpResponse
# Create your views here.

@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomProfileForm(instance=request.user.profile)
    return render(request, 'core/profile.html', {'form': form})

def login(request):
    next_url = request.POST.get('next') or request.GET.get('next', '')
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if next_url and url_has_allowed_host_and_scheme(
                url = next_url,
                allowed_hosts = {request.get_host()},
                require_https = request.is_secure(),
            ): return redirect(next_url)
            return redirect('index')
    else:
        form = CustomLoginForm()
    return render(request, 'core/login.html', {'form': form, 'next': next_url})

def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = CustomSignupForm()
    return render(request, 'core/signup.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect(request.META.get('HTTP_REFERER', 'index'))