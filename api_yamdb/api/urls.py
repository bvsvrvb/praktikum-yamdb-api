from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ReviewViewSet, CommentViewSet, TitleViewSet, UserViewSet,
    GenreViewSet, CategoryViewSet, signup, get_token
)

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')
router.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', signup),
    path('auth/token/', get_token),
]
