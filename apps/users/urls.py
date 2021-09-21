from django.urls import path
from apps.users.views import activate, logout, UserProfileTemplateView,\
    UserAuthView, UserLoginView, UserChangeView

app_name = 'users'

urlpatterns = [
    path('user-profile/', UserProfileTemplateView.as_view(), name='user_profile'),
    path('user-change/<int:pk>', UserChangeView.as_view(), name='user_change'),
    path('user-create/', UserAuthView.as_view(), name='user_create'),
    path('user-login/', UserLoginView.as_view(), name='user_login'),
    path(r'backend/activate/(?P<uid64>[0-9A-Za-z_-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         activate, name='activate'),
]