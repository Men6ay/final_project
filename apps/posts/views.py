from django.urls import reverse_lazy
from django.views import generic
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, generics, permissions, filters

from apps.posts.models import Post, Like, PostImage, PostVideo, Tag
from apps.posts.serializers import PostVideoSerializer, PostSerializer, \
    PostDetailSerializer, LikeSerializer, PostImageSerializer, TagSerializer
from apps.posts.permissions import OwnerPermission
from apps.posts.forms import PostLikeForm, PostCreateForm
from apps.posts.services import PostServices


class PostListView(generic.ListView):
    template_name = 'post_list.html'
    model = Post
    queryset = Post.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostListView, self).get_context_data()
        return PostServices.post_list(context)


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        return PostServices.post_detail(context, kwargs)


class PostCreateFormView(generic.FormView):
    form_class = PostCreateForm
    template_name = 'post_create.html'
    success_url = reverse_lazy('users:post_list')

    def get_context_data(self, **kwargs):
        context = super(PostCreateFormView, self).get_context_data()
        context['tags'] = Tag.objects.all()
        return context

    def form_valid(self, form):
        PostServices.post_create(self.request, form)
        return super(PostCreateFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(PostCreateFormView, self).form_invalid(form)


class PostLikeFormView(generic.FormView):
    form_class = PostLikeForm
    template_name = 'post_detail.html'
    success_url = reverse_lazy('users:post_list')

    def form_valid(self, form):
        PostServices.like_create(self.request, form)
        return super(PostLikeFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(PostLikeFormView, self).form_invalid(form)


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
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class LikeCreateAPIView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostImageAPIViewSet(viewsets.ModelViewSet):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer


class TagAPIViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PostVideoAPIViewSet(viewsets.ModelViewSet):
    queryset = PostVideo.objects.all()
    serializer_class = PostVideoSerializer
