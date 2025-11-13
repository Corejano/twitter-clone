import uuid
from django.db import models
from django.conf import settings


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    content = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes_count = models.IntegerField(default=0)
    retweets_count = models.IntegerField(default=0)
    replies_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'posts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['author', '-created_at']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f'{self.author.username}: {self.content[:50]}'

    def update_likes_count(self):
        self.likes_count = self.likes.count()
        self.save(update_fields=['likes_count'])


class PostImage(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='post_images/')
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'post_images'
        ordering = ['order']
        indexes = [
            models.Index(fields=['post', 'order']),
        ]

    def __str__(self):
        return f'Image {self.order} for post {self.post.id}'


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'likes'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'],
                name='unique_like'
            )
        ]
        indexes = [
            models.Index(fields=['user', 'post']),
            models.Index(fields=['post', '-created_at']),
        ]

    def __str__(self):
        return f'{self.user.username} likes post {self.post.id}'
