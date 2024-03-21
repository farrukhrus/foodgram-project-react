import django_filters

from recipe.models import Recipe, Favorite, Shopping


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug',
    )
    author = django_filters.NumberFilter(
        field_name='author__id',
    )
    is_favorited = django_filters.BooleanFilter(
        field_name='is_favorited'
    )
    is_in_shopping_cart = django_filters.NumberFilter(
        field_name='shoppings',
        method='filter_shopping'
    )

    def filter_favorite(self, queryset, name, value):
        if value == 1:
            return queryset.filter(
                id__in=Favorite.objects.filter(
                    user=self.request.user
                ).values_list('recipe', flat=True))
        return queryset

    def filter_shopping(self, queryset, name, value):
        if value == 1:
            return queryset.filter(
                id__in=Shopping.objects.filter(
                    user=self.request.user
                ).values_list('recipe', flat=True))
        return queryset

    class Meta:
        model = Recipe
        fields = ('author',
                  'tags',
                  'is_favorited',
                  'is_in_shopping_cart'
                  )
