from re import M
from rest_framework import serializers
from apps.posts.models import Post,Like,PostImage,Tag,PostVideo

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Like
        fields = "__all__"

class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImage
        fields = "__all__"

class PostVideoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PostVideo
        fields = "__all__"

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    total_likes = serializers.SerializerMethodField()
    post_images = PostImageSerializer(read_only=True, many=True)
    post_video = PostVideoSerializer(read_only=True, many = True)

    class Meta:
        model = Post
        fields = '__all__'

    def get_total_likes(self, instance):
        return instance.like_post.all().count()


class PostDetailSerializer(serializers.ModelSerializer):    

    class Meta:
        model = Post
        fields = "__all__"


