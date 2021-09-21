from django.db import IntegrityError

from apps.posts.models import Post, PostImage, PostVideo, Like


class PostServices:
    @staticmethod
    def post_create(request, form):
        title = form.cleaned_data.get('title')
        description = form.cleaned_data.get('description')
        images = request.FILES.getlist('images')
        videos = request.FILES.getlist('videos')
        tags = form.cleaned_data.get('tags')
        post = Post.objects.create(
            user=request.user,
            title=title,
            description=description,
        )
        post.tags.add(*tags)
        image_objects = []
        for image in images:
            image = PostImage(
                image=image, post=post
            )
            image_objects.append(image)
        PostImage.objects.bulk_create(image_objects)
        video_objects = []
        for video in videos:
            video = PostVideo(
                video=video, post=post
            )
            video_objects.append(video)
        PostVideo.objects.bulk_create(video_objects)

    @staticmethod
    def post_detail(context, kwargs):
        post_id = kwargs['object'].id
        images = PostImage.objects.filter(post_id=post_id)
        videos = PostVideo.objects.filter(post_id=post_id)
        context['images'] = images
        context['videos'] = videos
        return context

    @staticmethod
    def post_list(context):
        images = PostImage.objects.all()
        posts = Post.objects.filter(post_images__in=images).distinct()
        images = PostImage.objects.filter(post__in=posts)
        objects = zip(posts, images)
        context['objects'] = objects
        return context

    @staticmethod
    def like_create(request, form):
        post_id = form.cleaned_data['post_id']
        try:
            Like.objects.create(user_id=request.user.id, post_id=post_id)
        except IntegrityError:
            Like.objects.get(user_id=request.user.id, post_id=post_id).delete()
