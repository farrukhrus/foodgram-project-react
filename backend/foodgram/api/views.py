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
    CreateFollowSerializer,
    CustomUserSerializer,
)
from .permissions import IsAuthor
from .filters import RecipeFilter, IngredientFilter
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
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(
        detail=False,
        methods=['GET'],
        url_path='me',
        url_name='me',
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = get_object_or_404(User, id=self.request.user.id)
        serializer = CustomUserSerializer(
            user,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['POST'],
        url_name='subscribe',
        url_path='subscribe',
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id):

        context = {'request': request}
        usersubscribe = get_object_or_404(User, id=id)
        data = {
            'user': usersubscribe.id,
            'subscriber': request.user.id
        }
        serializer = CreateFollowSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def destroy_subscribe(self, request, id):
        subscribe = Subscription.objects.filter(
            user=get_object_or_404(User, id=id),
            subscriber=request.user.id
        )
        if subscribe.exists():
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['GET'],
        url_name='subscriptions',
        url_path='subscriptions',
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(
            following__subscriber=self.request.user.id
        )
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = IngredientFilter
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
        return generate_shopping_cart(self, request)


class FavoriteViewSet(CreateDestroyViewSet):
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.select_related('user').all()


class ShoppingViewSet(CreateDestroyViewSet):
    serializer_class = ShoppingSerializer
    queryset = Shopping.objects.select_related('user').all()
