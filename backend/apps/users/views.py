from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q

from apps.users.models import User, Follow
from apps.users.serializers import (
    UserSerializer,
    UserListSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer,
    LoginSerializer,
    FollowSerializer
)
from apps.users.services import UserService, FollowService
from apps.users.permissions import IsOwnerOrReadOnly


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'search':
            return UserListSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'list', 'search']:
            return [AllowAny()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['patch'])
    def update_me(self, request):
        serializer = UserUpdateSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(request.user, context={'request': request}).data)

    @action(detail=True, methods=['get'])
    def followers(self, request, username=None):
        user = UserService.get_user_by_username(username)
        followers = FollowService.get_followers(user)
        serializer = UserListSerializer(
            followers,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def following(self, request, username=None):
        user = UserService.get_user_by_username(username)
        following = FollowService.get_following(user)
        serializer = UserListSerializer(
            following,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def follow(self, request, username=None):
        user_to_follow = UserService.get_user_by_username(username)

        if request.user == user_to_follow:
            return Response(
                {'error': 'Cannot follow yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            follow, created = FollowService.follow_user(request.user, user_to_follow)
            if created:
                return Response(
                    {'message': f'Successfully followed {username}.'},
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {'message': f'Already following {username}.'},
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['delete'])
    def unfollow(self, request, username=None):
        user_to_unfollow = UserService.get_user_by_username(username)

        if FollowService.unfollow_user(request.user, user_to_unfollow):
            return Response(
                {'message': f'Successfully unfollowed {username}.'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'error': f'Not following {username}.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response([])

        users = User.objects.filter(
            Q(username__icontains=query) | Q(full_name__icontains=query)
        )[:20]

        serializer = UserListSerializer(
            users,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
