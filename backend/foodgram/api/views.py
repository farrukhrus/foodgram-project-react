from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    viewsets,
    mixins,
    filters,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from djoser.views import UserViewSet

from recipe.models import (
    Recipe,
    Ingredient,
    Tag,
    Subscription,
    Favorite,
    Shopping
)
from .serializers import (
    RecipeReadSerializer,
    RecipeWriteSerializer,
    TagSerializer,
    IngredientSerializer,
    FavoriteSerializer,
    SubscriptionSerializer,
    ShoppingSerializer,
)
from .permissions import IsAuthor
from .filters import RecipeFilter
from .utils import generate_shopping_cart


User = get_user_model()


class CreateDestroyViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    @action(methods=['DELETE'], detail=True)
    def delete(self, request, *args, **kwargs):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
        if not self.queryset.filter(user=user, recipe=recipe).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        self.queryset.get(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'limit'


class CustomUserViewSet(UserViewSet):
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @action(
        methods=['GET'],
        detail=False,
        url_name='subscriptions',
        url_path='subscriptions',
        permission_classes=[IsAuthenticated],
        pagination_class=CustomPagination
    )
    def get_subscription(self, request):
        limit = request.GET.get('recipes_limit', None)
        user = self.request.user
        subscriptions = Subscription.objects.filter(user=user)
        page = self.paginate_queryset(subscriptions)
        if page is not None:
            serializer = SubscriptionSerializer(
                page,
                many=True,
                context={
                    'recipes_limit': limit
                }
            )
            return self.get_paginated_response(serializer.data)
        serializer = SubscriptionSerializer(
            Subscription.objects.filter(user=user),
            many=True,
            context={
                'recipes_limit': limit
            }
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = None
    filterset_fields = ('name',)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related(
        'author'
    ).all()
    permission_classes = (IsAuthor,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPagination
    ordering = ['-id']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['GET'],
        detail=False,
        url_name='download_shopping_cart',
        url_path='download_shopping_cart',
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        generate_shopping_cart(self, request)


class FavoriteViewSet(CreateDestroyViewSet):
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.select_related('user').all()


class SubsViewSet(CreateDestroyViewSet):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.select_related('user').all()
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        limit = self.request.GET.get('recipes_limit', None)
        context = super().get_serializer_context()
        context.update({
            'recipes_limit': limit,
        })
        return context

    @action(methods=['DELETE'], detail=True)
    def delete(self, request, *args, **kwargs):
        user = self.request.user
        subscriber = get_object_or_404(User, id=self.kwargs.get('id'))
        if not Subscription.objects.filter(
            user=user,
            subscriber=subscriber
        ).exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        Subscription.objects.get(user=user, subscriber=subscriber).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingViewSet(CreateDestroyViewSet):
    serializer_class = ShoppingSerializer
    queryset = Shopping.objects.select_related('user').all()
