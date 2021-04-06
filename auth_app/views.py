from django.shortcuts import render, redirect
from .forms import UserRegisterForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'auth_app/home.html', {})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'auth_app/register.html', {'form': form})


# @login_required
# def edit_profile(request):
#     if request.method == 'POST':
#         form = ProfileUpdateForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f'Your account has been updated')
#             return redirect('profile')
#     else:
#         form = ProfileUpdateForm(instance=request.user)
