from django.db import transaction
from django.shortcuts import get_object_or_404
from apps.posts.models import Post, Like
from apps.users.models import Follow


class PostService:
    @staticmethod
    def get_post_by_id(post_id):
        return get_object_or_404(
            Post.objects.select_related('author').prefetch_related('images'),
            id=post_id
        )

    @staticmethod
    @transaction.atomic
    def create_post(author, content, images=None):
        post = Post.objects.create(
            author=author,
            content=content
        )
        return post

    @staticmethod
    @transaction.atomic
    def delete_post(post):
        post.delete()

    @staticmethod
    def get_user_posts(user, limit=None):
        queryset = Post.objects.filter(author=user).select_related(
            'author'
        ).prefetch_related('images')

        if limit:
            queryset = queryset[:limit]

        return queryset

    @staticmethod
    def get_feed_posts(user, limit=None):
        following_ids = Follow.objects.filter(
            follower=user
        ).values_list('following_id', flat=True)

        queryset = Post.objects.filter(
            author_id__in=list(following_ids) + [user.id]
        ).select_related('author').prefetch_related('images')

        if limit:
            queryset = queryset[:limit]

        return queryset

    @staticmethod
    def get_all_posts(limit=None):
        queryset = Post.objects.all().select_related(
            'author'
        ).prefetch_related('images')

        if limit:
            queryset = queryset[:limit]

        return queryset


class LikeService:
    @staticmethod
    def is_liked(user, post):
        return Like.objects.filter(user=user, post=post).exists()

    @staticmethod
    @transaction.atomic
    def like_post(user, post):
        like, created = Like.objects.get_or_create(
            user=user,
            post=post
        )

        if created:
            post.update_likes_count()

        return like, created

    @staticmethod
    @transaction.atomic
    def unlike_post(user, post):
        deleted_count, _ = Like.objects.filter(
            user=user,
            post=post
        ).delete()

        if deleted_count > 0:
            post.update_likes_count()

        return deleted_count > 0

    @staticmethod
    def get_post_likes(post, limit=None):
        queryset = Like.objects.filter(post=post).select_related('user')

        if limit:
            queryset = queryset[:limit]

        return queryset

    @staticmethod
    def get_user_liked_posts(user, limit=None):
        queryset = Post.objects.filter(
            likes__user=user
        ).select_related('author').prefetch_related('images')

        if limit:
            queryset = queryset[:limit]

        return queryset
