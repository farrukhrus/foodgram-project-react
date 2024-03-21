from django.contrib import admin

from .models import Recipe, Ingredient, Tag, Favorite


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'author', 'image',
        'text', 'cooking_time', 'favorite_count'
    )
    list_filter = ('author', 'name', 'tags')
    filter_horizontal = ('tags', 'ingredients')
    search_fields = ['name', 'author__username']

    def favorite_count(self, obj):
        return Favorite.objects.filter(recipe_id=obj.id).count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    search_fields = ['name', 'slug']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ['user__username', 'user__email']
