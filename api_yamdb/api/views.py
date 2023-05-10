from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework import viewsets, status, filters
from django_filters import rest_framework as dj_filters
from rest_framework.decorators import api_view, action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.db.models import Avg

from .mixins import CreateListDestroyViewSet
from reviews.models import Title, User, Genre, Review, Category
from .filters import TitleFilter
from .utils import to_send_mail
from .serializers import (
    ReviewSerializer,
    UserSerializer,
    SignUpSerializer,
    GetTokenSerializer,
    TitleSerializer,
    CommentSerializer,
    GenreSerializer,
    CategorySerializer,
    PostTitleSerializer
)
from .permissions import (
    IsAdminUser,
    ReviewsCommentPermission,
    TitlesCategoriesGenresPermission
)


RANDOM_MIN = 100000
RANDOM_MAX = 999999
ALLOWED_METHODS = ('get', 'post', 'patch', 'delete',
                   'head', 'options', 'trace')


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (ReviewsCommentPermission,)
    pagination_class = LimitOffsetPagination
    http_method_names = ALLOWED_METHODS

    def get_title_object(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title_object().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title=self.get_title_object()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (ReviewsCommentPermission,)
    pagination_class = LimitOffsetPagination
    http_method_names = ALLOWED_METHODS

    def get_title_object(self):
        return get_object_or_404(
            Review, title__id=self.kwargs.get('title_id'),
            pk=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        return self.get_title_object().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, review=self.get_title_object()
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    pagination_class = LimitOffsetPagination
    http_method_names = ALLOWED_METHODS
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='me'
    )
    def me_page(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role, partial=True)

        serializer = UserSerializer(request.user)

        return Response(serializer.data)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (TitlesCategoriesGenresPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (TitlesCategoriesGenresPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (TitlesCategoriesGenresPermission,)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return PostTitleSerializer
        return TitleSerializer


@api_view(['POST'])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    email = request.data.get('email')
    username = request.data.get('username')

    if User.objects.filter(email=email, username=username).exists():
        user = User.objects.get(email=email)
        code = user.confirmation_code
        to_send_mail(code, email)
        return Response(
            {
                'message': (
                    'Эта электронная почта уже зарегистрирована. '
                    'Код отправлен повторно.'
                )
            }
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {'message': 'Пользователь с таким именем уже существует'},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    user = User.objects.create(username=username, email=email)
    code = default_token_generator.make_token(user)
    user.confirmation_code = code
    user.save()
    to_send_mail(code, email)

    return Response(serializer.data)


@api_view(['POST'])
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    token = AccessToken.for_user(user)
    return Response(f'Ваш токен: {token}')
