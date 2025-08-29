from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from .forms import CustomUserCreationForm

# Create your views here.

@require_http_methods(['GET', 'POST'])
def signup_signin(request):
    if request.user.is_authenticated:
        return redirect('main_app:index')

    signup_form = CustomUserCreationForm(request.POST)
    signin_form = AuthenticationForm(request, data=request.POST)

    if request.method == 'POST':
        if 'signup' in request.POST and signup_form.is_valid():
            user = signup_form.save()
            auth_login(request, user)
            return redirect('main_app:index')

        elif 'signin' in request.POST and signin_form.is_valid():
            user = signin_form.get_user()
            auth_login(request, user)
            return redirect('main_app:index')

    return render(request, 'accounts/signup_signin.html', {
        'signup_form': signup_form,
        'signin_form': signin_form,
    })

def signout(request):
    auth_logout(request)
    return redirect('main_app:index')