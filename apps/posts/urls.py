from rest_framework.routers import DefaultRouter
from apps.comments.views import CommentAPIView
from django.urls import path
from apps.posts.views import PostAPIViewSet,LikeCreateAPIView,PostImageAPIViewSet,TagAPIViewSet,PostVideoAPIViewSet
from apps.users.views import UserAPIView,activate

app_name = 'users'

router = DefaultRouter()
router.register('post', PostAPIViewSet, basename='post_api')
router.register('comment', CommentAPIView, basename='post_comment')
router.register('image', PostImageAPIViewSet, basename='post_image')
router.register('tags', TagAPIViewSet, basename='tags')
router.register('user', UserAPIView, basename='users')
router.register('video', PostVideoAPIViewSet, basename='videos')

urlpatterns = [
    path('like/', LikeCreateAPIView.as_view(), name='like'),
    path(r'backend/activate/(?P<uid64>[0-9A-Za-z_-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name = 'activate'),
]

urlpatterns += router.urls
