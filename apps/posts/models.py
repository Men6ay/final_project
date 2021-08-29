from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.deletion import CASCADE

User = get_user_model()

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
    def __str__(self):
        return f'{self.title} -- {self.create_at}'