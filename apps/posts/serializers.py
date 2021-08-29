from re import M
from rest_framework import serializers
from apps.posts.models import Post
from apps.users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class PostDetailSerializer(serializers.ModelSerializer):    

    class Meta:
        model = Post
        fields = "__all__"
