from django.urls import path
from apps.users.views import activate

urlpatterns = [
    path(r'backend/activate/(?P<uid64>[0-9A-Za-z_-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name = 'activate'),
]