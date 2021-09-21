from django.urls import path
from apps.posts import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>', views.PostDetail.as_view(), name='post_detail'),
    path('post-create/', views.PostCreateFormView.as_view(),
         name='post_create'),
    path('post-delete/<int:pk>', views.PostDeleteView.as_view(),
         name='post_delete'),
    path('post-like/', views.PostLikeFormView.as_view(), name='post_like'),
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    path('tag-create/', views.TagCreateFormView.as_view(), name='tag_create'),
    path('tag-delete/<int:pk>', views.TagDeleteView.as_view(),
         name='tag_delete'),
    path('comment-delete/<int:pk>', views.CommentDeleteView.as_view(),
         name='comment_delete'),
]
