import django_filters

from recipe.models import Recipe


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug',
    )
    author = django_filters.NumberFilter(
        field_name='author__id',
    )
    is_favorited = django_filters.BooleanFilter(
        field_name='favorites'
    )
    is_in_shopping_cart = django_filters.BooleanFilter(
        field_name='shoppings'
    )

    class Meta:
        model = Recipe
        fields = ('author',
                  'tags',
                  'is_favorited',
                  'is_in_shopping_cart'
                  )
