from django.db import transaction
from django.db import models
from django.shortcuts import get_object_or_404
from apps.users.models import User, Follow


class UserService:
    @staticmethod
    def get_user_by_username(username):
        return get_object_or_404(User, username=username)

    @staticmethod
    def get_user_by_id(user_id):
        return get_object_or_404(User, id=user_id)

    @staticmethod
    @transaction.atomic
    def create_user(username, email, full_name, password):
        user = User.objects.create_user(
            username=username,
            email=email,
            full_name=full_name,
            password=password
        )
        return user

    @staticmethod
    @transaction.atomic
    def update_user_profile(user, **kwargs):
        for field, value in kwargs.items():
            if hasattr(user, field):
                setattr(user, field, value)
        user.save()
        return user

    @staticmethod
    def search_users(query, limit=20):
        return User.objects.filter(
            models.Q(username__icontains=query) |
            models.Q(full_name__icontains=query)
        )[:limit]


class FollowService:
    @staticmethod
    def is_following(follower, following):
        return Follow.objects.filter(
            follower=follower,
            following=following
        ).exists()

    @staticmethod
    @transaction.atomic
    def follow_user(follower, following):
        if follower == following:
            raise ValueError('Cannot follow yourself.')

        follow, created = Follow.objects.get_or_create(
            follower=follower,
            following=following
        )
        return follow, created

    @staticmethod
    @transaction.atomic
    def unfollow_user(follower, following):
        deleted_count, _ = Follow.objects.filter(
            follower=follower,
            following=following
        ).delete()
        return deleted_count > 0

    @staticmethod
    def get_followers(user, limit=None):
        queryset = Follow.objects.filter(following=user).select_related('follower')
        if limit:
            queryset = queryset[:limit]
        return [follow.follower for follow in queryset]

    @staticmethod
    def get_following(user, limit=None):
        queryset = Follow.objects.filter(follower=user).select_related('following')
        if limit:
            queryset = queryset[:limit]
        return [follow.following for follow in queryset]
