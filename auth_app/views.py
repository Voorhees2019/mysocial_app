from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import UserRegisterForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def home(request):
    return render(request, 'auth_app/home.html', {})


def searchresult(request):
    if request.GET.get('q'):
        search = request.GET.get('q', ' ')
        search_result = User.objects.filter(username__icontains=search)
        return render(request, 'auth_app/search_result.html', {'search_result': search_result})
    else:
        return HttpResponse('Please submit a search form.')


def about(request):
    return render(request, 'auth_app/about.html', {})


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
# def profile(request):
#     return render(request, 'auth_app/profile.html', {})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(instance=request.user.profile)
        if 'editProfile' in request.POST:
            form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            if form.is_valid():
                form.save()
                messages.success(request, f'Your account has been updated')
                return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'auth_app/edit_profile.html', {'form': form})


@login_required
def user(request, username):
    user_obj = get_object_or_404(User, username=username)
    return render(request, 'auth_app/profile.html', {'user_obj': user_obj})

