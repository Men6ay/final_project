from django.urls import path
from apps.posts import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('post', views.PostAPIViewSet, basename='post_api')


urlpatterns = router.urls