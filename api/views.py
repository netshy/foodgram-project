import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from recipes.models import (Recipe, ShoppingList, SubscriptionsUsers,
                            FavoritesRecipes, User, Ingredient)


@require_http_methods(["POST"])
def add_recipe_shopping_list(request):
    if request.user.is_anonymous:
        return JsonResponse({'success': False}, status=400)

    json_data = json.loads(request.body)
    if ShoppingList.objects.filter(recipe=json_data.get('id'),
                                   user=request.user).exists():
        return JsonResponse({'success': False}, status=400)
    else:
        recipe = get_object_or_404(Recipe, pk=json_data.get('id'))
        ShoppingList.objects.create(recipe=recipe, user=request.user)
        return JsonResponse({'success': True})


@require_http_methods(["DELETE"])
def remove_recipe_shopping_list(request, recipe_id):
    if get_object_or_404(ShoppingList, recipe_id=recipe_id).delete()[0] != 0:
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)



@require_http_methods(["POST"])
def following(request):
    if request.user.is_anonymous:
        return JsonResponse({'success': False}, status=400)

    json_data = json.loads(request.body)
    if request.user.username == get_object_or_404(
            User, id=json_data.get('id')).username:
        return JsonResponse({'success': False}, status=400)
    else:
        SubscriptionsUsers.objects.create(author_id=json_data.get('id'),
                                          user_id=request.user.id)
        return JsonResponse({'success': True})


@require_http_methods(["DELETE"])
def unfollowing(request, author_id):
    if get_object_or_404(ShoppingList, author_id=author_id,
                         user_id=request.user.id).delete()[0] != 0:
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@require_http_methods(["POST"])
def add_favorite_recipe(request):
    json_data = json.loads(request.body)
    if FavoritesRecipes.objects.filter(favorites_id=json_data.get('id'),
                                       user_id=request.user.id).exists():
        return JsonResponse({'success': False}, status=400)
    else:
        FavoritesRecipes.objects.create(favorites_id=json_data.get('id'),
                                        user_id=request.user.id)
        return JsonResponse({'success': True})


@require_http_methods(["DELETE"])
def remove_favorite_recipe(request, recipe_id):
    if get_object_or_404(FavoritesRecipes, favorites_id=recipe_id,
                         user_id=request.user.id).delete()[0] != 0:
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@require_http_methods(["GET"])
def parse_ingredients(request):
    query = request.GET.get('query', [])
    ingredients_query = Ingredient.objects.filter(
        title__istartswith=query
    ).values('title', 'dimension')

    response = list(ingredients_query)
    return JsonResponse(response, safe=False)
