from django.db.models import F

from recipes.models import Recipe


def count_recipe_favorites(json_data):
    recipe = Recipe.objects.get(pk=json_data.get('id'))
    recipe.counter = F('counter') + 1
    recipe.save(update_fields=['counter'])
