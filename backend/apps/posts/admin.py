from django.contrib import admin
from apps.posts.models import Post, PostImage, Like


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1
    fields = ['image', 'order']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'content_preview', 'created_at', 'likes_count']
    list_filter = ['created_at']
    search_fields = ['author__username', 'content']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'likes_count', 'retweets_count', 'replies_count']
    inlines = [PostImageInline]

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'order', 'image']
    list_filter = ['post']
    ordering = ['post', 'order']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__content']
    ordering = ['-created_at']
