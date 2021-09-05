from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.deletion import CASCADE
from apps.posts.models import Post

User = get_user_model()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comment')
    post = models.ForeignKey(Post, on_delete=CASCADE,related_name='comment_post')
    text = models.TextField(blank=True,null=True)
    
    def __str__(self):
        return f"{self.user} -- {self.post.id}"

