from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    title = models.CharField(max_length=250, blank=True)
    image = models.ImageField(upload_to='post_images')
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return f'{self.author} - {self.title[:30]}'

    @property
    def number_of_likes(self):
        return Like.objects.filter(post=self).count()


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liker')

    def __str__(self):
        return f'{self.user} liked {self.post.title}'
