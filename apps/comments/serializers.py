from rest_framework import serializers
from apps.comments.models import Comment
from re import M

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"