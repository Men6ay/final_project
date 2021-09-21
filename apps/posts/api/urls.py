from django.urls import path

from rest_framework.routers import DefaultRouter

from apps.comments.views import CommentAPIView
from apps.posts.api.views import PostAPIViewSet, LikeCreateAPIView,\
    PostImageAPIViewSet, TagAPIViewSet, PostVideoAPIViewSet
from apps.users.views import UserAPIView


router = DefaultRouter()
router.register('post', PostAPIViewSet, basename='post_api')
router.register('comment', CommentAPIView, basename='post_comment')
router.register('image', PostImageAPIViewSet, basename='post_image')
router.register('tags', TagAPIViewSet, basename='tags')
router.register('user', UserAPIView, basename='users')
router.register('video', PostVideoAPIViewSet, basename='videos')

urlpatterns = [
    path('like/', LikeCreateAPIView.as_view(), name='like'),
]
urlpatterns += router.urls

