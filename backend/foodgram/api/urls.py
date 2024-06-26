from rest_framework import routers
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from api.views import (
    TagViewSet,
    CustomUserViewSet,
    RecipeViewSet,
    IngredientViewSet,
    FavoriteViewSet,
    ShoppingViewSet,
)

router = routers.DefaultRouter()
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'recipes', RecipeViewSet, basename='recipe')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(
    r'recipes/(?P<id>\d+)/favorite',
    FavoriteViewSet,
    basename='favorite'
)
router.register('users', CustomUserViewSet, basename='subscribe')
router.register(
    r'recipes/(?P<id>\d+)/shopping_cart',
    ShoppingViewSet,
    basename='shopping'
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
