import django_filters

from recipe.models import Recipe, Favorite, Shopping, Ingredient


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug',
    )
    author = django_filters.NumberFilter(
        field_name='author__id',
    )
    is_favorited = django_filters.NumberFilter(
        field_name='favorites',
        method='filter_favorites'
    )
    is_in_shopping_cart = django_filters.NumberFilter(
        field_name='shoppings',
        method='filter_shoppings'
    )

    def filter_favorites(self, queryset, name, value):
        user = self.request.user
        if value == 1:
            return queryset.filter(id__in=Favorite.objects.filter(
                user=user
            ).values_list('recipe', flat=True))
        return queryset

    def filter_shoppings(self, queryset, name, value):
        user = self.request.user
        if value == 1:
            return queryset.filter(id__in=Shopping.objects.filter(
                user=user
            ).values_list('recipe', flat=True))
        return queryset

    class Meta:
        model = Recipe
        fields = ('author',
                  'tags',
                  'is_favorited',
                  'is_in_shopping_cart'
                  )
