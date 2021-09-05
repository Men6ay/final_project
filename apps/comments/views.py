from django.shortcuts import render
from apps.comments.models import Comment
from apps.comments.serializers import CommentSerializer
from apps.posts.permissions import OwnerPermission
from rest_framework import viewsets,permissions

class CommentAPIView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()        
    serializer_class = CommentSerializer
    permission_classes = [
        OwnerPermission,
    ]
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permission() for permission in self.permission_classes]

