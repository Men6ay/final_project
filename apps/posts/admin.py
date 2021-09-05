from django.contrib import admin
from apps.posts.models import Post,Like,PostImage,PostVideo,Tag

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(PostImage)
admin.site.register(PostVideo)
admin.site.register(Tag)
