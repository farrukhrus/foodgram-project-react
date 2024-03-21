from django.http import HttpResponse
from django.db.models import Sum

from recipe.models import Shopping, Ingredient, IngredientRecipe


def generate_shopping_cart(self, request):
    user = self.request.user
    shopping = Shopping.objects.filter(user=user).values_list(
        'recipe',
        flat=True
    )
    lines = []
    file_name = 'shopping_cart.txt'
    lines.append('Список покупок:\n')
    ingredients = IngredientRecipe.objects.filter(
        recipe_id__in=shopping
    ).values('ingredient').annotate(totals=Sum('amount'))
    for ingredient in ingredients:
        lines.append('{0} - {1}'.format(
            Ingredient.objects.get(id=ingredient['ingredient']),
            ingredient['totals']
        )
        )
    response_content = '\n'.join(lines)
    response = HttpResponse(response_content, content_type="text")
    response['Content-Disposition'] = 'attachment; filename={0}'.format(
        file_name
    )
    return response
