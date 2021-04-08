from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def posts(request):
    return render(request, 'posts_app/posts.html', {})
