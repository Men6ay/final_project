from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=255,
        db_index=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, default=None
    )

    def __str__(self):
        return f'{self.id} -- {self.name}'


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(
        max_length=255, blank=True,
        null=True, db_index=True,
    )
    description = models.TextField(
        blank=True, null=True
    )
    create_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='post_tags')

    def __str__(self):
        return f'{self.title} -- {self.create_at}'


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='like_user'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        related_name='like_post',
    )

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.id}"


class PostImage(models.Model):
    image = models.ImageField(
        upload_to='images'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        related_name='post_images',
    )

    def __str__(self):
        return f"{self.id} == {self.post.title}"


class PostVideo(models.Model):
    video = models.FileField(upload_to='video')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='post_video')

    def __str__(self):
        return f'{self.id} {self.post.title}'
