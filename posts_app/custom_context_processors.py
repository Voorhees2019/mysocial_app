from .forms import PostForm


def post_form_renderer(request):
    post_form = PostForm()
    if request.method == 'POST':
        if 'addNewPost' in request.POST:
            post_form = PostForm(request.POST, request.FILES)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.author = request.user
                post.save()
    return {'post_form': post_form}
