from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from auth_app.models import Follow
from .models import Post, Like
from django.views.generic import ListView, DetailView
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
import random


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts_app/posts.html'
    context_object_name = 'posts'
    paginate_by = 7

    def get_queryset(self):
        following_list = Follow.objects.filter(follower=self.request.user)
        posts_obj = Post.objects.filter(author__in=following_list.values_list('following')).order_by('-date_posted')

        following_post_number = 0
        for i in following_list:
            following_post_number += i.following.post.count()

        # recommend random users if there are not many posts to show (or few followings)
        if User.objects.all().count() >= 5:
            if following_post_number < 5 or len(following_list) < 3:
                recommended_users = set()
                while len(recommended_users) < 3:
                    last_user = User.objects.count() - 1
                    appropriate_pseudo_user = False

                    while not appropriate_pseudo_user:
                        r = random.randint(0, last_user)
                        recommended_user = User.objects.all()[r]

                        # if already following recommended_user pick another random one
                        if not following_list.filter(following=recommended_user)\
                                and recommended_user != self.request.user:
                            appropriate_pseudo_user = True

                    recommended_users.add(recommended_user)
                    posts_obj |= Post.objects.filter(author=recommended_user)[:5]
                    posts_obj.order_by('-date_posted')
        return posts_obj

    def post(self, request, *args, **kwargs):
        if 'addNewPost' in request.POST:
            post_form = PostForm(request.POST, request.FILES)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.author = request.user
                post.save()
        return self.get(self, request, *args, **kwargs)


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        already_liked = Like.objects.filter(post=self.get_object(), user=self.request.user)
        context['already_liked'] = already_liked
        return context


@login_required
def like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    already_liked = Like.objects.filter(post=post, user=request.user)
    if not already_liked:
        post_like = Like(post=post, user=request.user)
        post_like.save()
    return redirect('post-detail', pk=post.id)


@login_required
def unlike(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    already_liked = Like.objects.filter(post=post, user=request.user)
    already_liked.delete()
    return redirect('post-detail', pk=post.id)
