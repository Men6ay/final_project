from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from apps.comments.models import Comment
from apps.posts.models import Post, Tag
from apps.posts.forms import PostLikeForm, PostCreateForm, TagCreateForm, \
    CommentCreationForm
from apps.posts.services import PostServices


class PostListView(generic.ListView):
    template_name = 'post_list.html'
    model = Post
    queryset = Post.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostListView, self).get_context_data()
        return PostServices.post_list(context)


class PostDetail(generic.DetailView, generic.FormView):
    model = Post
    form_class = CommentCreationForm
    template_name = 'post_detail.html'
    success_url = reverse_lazy('posts:post_list')

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        post = kwargs.get('object')
        context['comments'] = Comment.objects.filter(post_id=post.id)
        return PostServices.post_detail(context, kwargs)

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            Comment.objects.create(
                user_id=self.request.user.id,
                post_id=form.cleaned_data.get('post'),
                text=form.cleaned_data.get('text')
            )
        else:
            return super(PostDetail, self).form_invalid(form)
        return super(PostDetail, self).form_valid(form)

    def form_invalid(self, form):
        return super(PostDetail, self).form_invalid(form)


class PostCreateFormView(generic.FormView):
    form_class = PostCreateForm
    template_name = 'post_create.html'
    success_url = reverse_lazy('posts:post_list')

    def get_context_data(self, **kwargs):
        context = super(PostCreateFormView, self).get_context_data()
        context['tags'] = Tag.objects.all()
        return context

    def form_valid(self, form):
        PostServices.post_create(self.request, form)
        return super(PostCreateFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(PostCreateFormView, self).form_invalid(form)


class PostUpdateView(generic.UpdateView):
    model = Post
    fields = ('title', 'description', 'tags', )
    template_name = 'post_update.html'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('posts:post_list')

    def form_valid(self, form):
        user = self.request.user
        if user and self.get_object().user == user:
            form.save(commit=True)
        else:
            return HttpResponse('You have no permissions.')
        return super(PostUpdateView, self).form_valid(form)


class PostDeleteView(generic.DeleteView):
    model = Post
    success_url = reverse_lazy('posts:post_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs['pk'])
        if request.user == post.user:
            return super(PostDeleteView, self).dispatch(
                request, *args, **kwargs
            )
        else:
            return HttpResponse('You have no permissions')


class CommentDeleteView(generic.DeleteView):
    model = Comment
    success_url = reverse_lazy('posts:post_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        comment = Comment.objects.get(id=kwargs['pk'])
        if request.user == comment.user:
            return super(CommentDeleteView, self).dispatch(
                request, *args, **kwargs
            )
        else:
            return HttpResponse('You have no permissions')


class CommentUpdateView(generic.UpdateView):
    model = Comment
    fields = ('text', )
    template_name = 'comment_update.html'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('posts:post_list')

    def form_valid(self, form):
        user = self.request.user
        if user and self.get_object().user == user:
            form.save(commit=True)
        else:
            return HttpResponse('You have no permissions.')
        return super(CommentUpdateView, self).form_valid(form)


class TagListView(generic.ListView):
    template_name = 'tags_list.html'
    model = Tag

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TagListView, self).get_context_data()
        context['tags'] = Tag.objects.all()
        return context


class TagCreateFormView(generic.FormView):
    form_class = TagCreateForm
    template_name = 'tags_create.html'
    success_url = reverse_lazy('posts:tag_list')

    def form_valid(self, form):
        user = self.request.user
        if user:
            tag = form.save(commit=True)
            tag.user = user
            tag.save()
        else:
            return HttpResponse('You have no permissions.')
        return super(TagCreateFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(TagCreateFormView, self).form_invalid(form)


class TagUpdateView(generic.UpdateView):
    model = Tag
    fields = ('name', )
    template_name = 'tag_update.html'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('posts:tag_list')

    def form_valid(self, form):
        user = self.request.user
        if user and self.get_object().user == user:
            form.save(commit=True)
        else:
            return HttpResponse('You have no permissions.')
        return super(TagUpdateView, self).form_valid(form)


class TagDeleteView(generic.DeleteView):
    model = Tag
    success_url = reverse_lazy('posts:tag_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user == self.request.user:
            return super(TagDeleteView, self).dispatch(
                request, *args, **kwargs
            )
        else:
            return HttpResponse('You have no permissions')


class PostLikeFormView(generic.FormView):
    form_class = PostLikeForm
    template_name = 'post_detail.html'
    success_url = reverse_lazy('posts:post_list')

    def form_valid(self, form):
        PostServices.like_create(self.request, form)
        return super(PostLikeFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(PostLikeFormView, self).form_invalid(form)

