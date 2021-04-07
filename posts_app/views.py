from django.shortcuts import render


def home(request):
    return render(request, 'posts_app/home.html', {})

