from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

from apps.posts.models import Post, Like
from apps.posts.serializers import (
    PostSerializer,
    PostCreateSerializer,
    PostListSerializer,
    LikeSerializer
)
from apps.posts.services import PostService, LikeService
from apps.posts.permissions import IsAuthorOrReadOnly


class PostPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PostPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        elif self.action == 'list':
            return PostListSerializer
        return PostSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'likes']:
            return [AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAuthorOrReadOnly()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = Post.objects.all().select_related(
            'author'
        ).prefetch_related('images')
        return queryset

    def list(self, request):
        posts = PostService.get_feed_posts(request.user)
        page = self.paginate_queryset(posts)

        if page is not None:
            serializer = PostListSerializer(
                page,
                many=True,
                context={'request': request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = PostListSerializer(
            posts,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    @method_decorator(ratelimit(key='user', rate='10/m', method='POST'))
    def create(self, request):
        serializer = PostCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save(author=request.user)

        response_serializer = PostSerializer(
            post,
            context={'request': request}
        )
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk=None):
        post = PostService.get_post_by_id(pk)
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        post = PostService.get_post_by_id(pk)

        if post.author != request.user:
            return Response(
                {'error': 'You can only delete your own posts.'},
                status=status.HTTP_403_FORBIDDEN
            )

        PostService.delete_post(post)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @method_decorator(ratelimit(key='user', rate='30/m', method=['POST', 'DELETE']))
    @action(detail=True, methods=['post', 'delete'])
    def like(self, request, pk=None):
        post = PostService.get_post_by_id(pk)

        if request.method == 'POST':
            like, created = LikeService.like_post(request.user, post)

            if created:
                return Response(
                    {'message': 'Post liked successfully.'},
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {'message': 'Post already liked.'},
                status=status.HTTP_200_OK
            )
        elif request.method == 'DELETE':
            if LikeService.unlike_post(request.user, post):
                return Response(
                    {'message': 'Post unliked successfully.'},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'error': 'Post was not liked.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        post = PostService.get_post_by_id(pk)
        likes = LikeService.get_post_likes(post)

        page = self.paginate_queryset(likes)
        if page is not None:
            serializer = LikeSerializer(
                page,
                many=True,
                context={'request': request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = LikeSerializer(
            likes,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
