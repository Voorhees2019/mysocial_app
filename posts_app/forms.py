from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'title']


class PostCommentForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 5}))

    class Meta:
        model = Comment
        fields = ['content']
