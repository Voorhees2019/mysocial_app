from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import UserRegisterForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Follow


def home(request):
    return render(request, 'auth_app/home.html', {})


def searchresult(request):
    if request.GET.get('q'):
        search = request.GET.get('q', ' ')
        search_result = User.objects.filter(username__icontains=search)
        return render(request, 'auth_app/search_result.html', {'search_result': search_result})
    else:
        return HttpResponse('Please submit a search form.')


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


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(instance=request.user.profile)
        if 'editProfile' in request.POST:
            form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            if form.is_valid():
                form.save()
                messages.success(request, f'Your account has been updated')
                return redirect('user-profile', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'auth_app/edit_profile.html', {'form': form})


@login_required
def user(request, username):
    user_obj = get_object_or_404(User, username=username)
    following_own_profile = False
    if request.user.username == username:
        following_own_profile = True
    already_followed = Follow.objects.filter(follower=request.user, following=user_obj)
    return render(request, 'auth_app/profile.html', {
        'user_obj': user_obj,
        'already_followed': already_followed,
        'following_own_profile': following_own_profile
    })


@login_required
def follow(request, username):
    following = get_object_or_404(User, username=username)
    follower = request.user
    already_followed = Follow.objects.filter(follower=follower, following=following)
    if not already_followed:
        followed_user = Follow(follower=follower, following=following)
        followed_user.save()
    return redirect('user-profile', username=username)


@login_required
def unfollow(request, username):
    following = get_object_or_404(User, username=username)
    follower = request.user
    already_followed = Follow.objects.filter(follower=follower, following=following)
    already_followed.delete()
    return redirect('user-profile', username=username)

