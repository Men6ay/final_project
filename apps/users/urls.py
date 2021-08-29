from rest_framework.routers import DefaultRouter
from apps.users import views
from django.urls import path

app_name = 'users'

router = DefaultRouter()
router.register('user', views.UserAPIView, basename='users')

urlpatterns = [
    path('activate/<str:email>/', views.activate, name = 'activate'),
]
urlpatterns += router.urls