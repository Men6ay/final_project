from django.shortcuts import render
from apps.posts.models import Post,Like,PostImage, PostVideo,Tag
from apps.posts.serializers import PostVideoSerializer,PostSerializer,PostDetailSerializer,LikeSerializer,PostImageSerializer,TagSerializer
from apps.posts.permissions import OwnerPermission
from rest_framework import viewsets, generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

class PostAPIViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = [
        'user__username', 'title',
    ]
    ordering_fields = [
        'user', 'title', 
    ]

    permission_classes = [
        OwnerPermission,
    ]

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return PostDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permission() for permission in self.permission_classes]

class LikeCreateAPIView(generics.ListCreateAPIView):

    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

class PostImageAPIViewSet(viewsets.ModelViewSet):

    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer

class TagAPIViewSet(viewsets.ModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    
class PostVideoAPIViewSet(viewsets.ModelViewSet):
    
    queryset = PostVideo.objects.all()
    serializer_class = PostVideoSerializer



