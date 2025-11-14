from rest_framework import serializers
from apps.posts.models import Post, PostImage, Like
from apps.users.serializers import UserListSerializer


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'image', 'order']
        read_only_fields = ['id']


class PostSerializer(serializers.ModelSerializer):
    author = UserListSerializer(read_only=True)
    images = PostImageSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'content', 'created_at', 'updated_at',
            'likes_count', 'retweets_count', 'replies_count',
            'images', 'is_liked'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at',
            'likes_count', 'retweets_count', 'replies_count'
        ]

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(
                user=request.user,
                post=obj
            ).exists()
        return False


class PostCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        required=False,
        allow_empty=True,
        max_length=4
    )

    class Meta:
        model = Post
        fields = ['content', 'images']

    def validate_content(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Content cannot be empty.')
        if len(value) > 280:
            raise serializers.ValidationError('Content must not exceed 280 characters.')
        return value

    def validate_images(self, value):
        if len(value) > 4:
            raise serializers.ValidationError('Cannot upload more than 4 images.')

        for image in value:
            if image.size > 5 * 1024 * 1024:
                raise serializers.ValidationError('Each image must not exceed 5MB.')

        return value

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        post = Post.objects.create(**validated_data)

        for index, image in enumerate(images_data):
            PostImage.objects.create(
                post=post,
                image=image,
                order=index
            )

        return post


class PostListSerializer(serializers.ModelSerializer):
    author = UserListSerializer(read_only=True)
    images = PostImageSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'content', 'created_at',
            'likes_count', 'retweets_count', 'replies_count',
            'images', 'is_liked'
        ]

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(
                user=request.user,
                post=obj
            ).exists()
        return False


class LikeSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['id', 'created_at']
