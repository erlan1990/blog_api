from django.db import models
from post.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()

class Comment(models.Model):
    body = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    author = models.ForeignKey(User, on_delete=models. CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' comment from {self.author.name} to {self.post.title}'
    

class Rating(models.Model):
    rating = models.PositiveSmallIntegerField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='rating')
    author = models.ForeignKey(User, on_delete=models. CASCADE, related_name='rating')

    def __str__(self):
        return f'{self.rating} - {self.post}'
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(User, on_delete=models. CASCADE, related_name='likes')

    def __str__(self):
        return f'{self.post} liked by {self.author}'

