import json

from django import http
from django.http import JsonResponse

from api.utils import count_recipe_favorites
from recipes.models import Recipe, ShoppingList, SubscriptionsUsers, \
    FavoritesRecipes, User, Ingredient


def add_recipe_shopping_list(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        if ShoppingList.objects.filter(recipe=json_data.get('id'),
                                       user=request.user).exists():
            return http.HttpResponse(status=400,
                                     content_type='application/json')
        else:

            recipe = Recipe.objects.get(pk=json_data.get('id'))
            ShoppingList.objects.create(recipe=recipe, user=request.user)
            return JsonResponse({'success': True})

    return http.HttpResponse(status=405, content_type='application/json')


def remove_recipe_shopping_list(request, recipe_id):
    if request.method == 'DELETE':
        ShoppingList.objects.get(recipe_id=recipe_id).delete()
        return JsonResponse({'success': True})
    return http.HttpResponse(status=405, content_type='application/json')


def following(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        if request.user.username == User.objects.get(
                id=json_data.get('id')).username:
            return http.HttpResponse(status=400,
                                     content_type='application/json')
        else:
            SubscriptionsUsers.objects.create(author_id=json_data.get('id'),
                                              user_id=request.user.id)
            return JsonResponse({'success': True})
    return http.HttpResponse(status=405, content_type='application/json')


def unfollowing(request, author_id):
    if request.method == 'DELETE':
        if SubscriptionsUsers.objects.filter(author_id=author_id,
                                             user_id=request.user.id).exists():
            SubscriptionsUsers.objects.get(author_id=author_id,
                                           user_id=request.user.id).delete()
            return JsonResponse({'success': True})
        return http.HttpResponse(status=400,
                                 content_type='application/json')
    return http.HttpResponse(status=405, content_type='application/json')


def add_favorite_recipe(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        if FavoritesRecipes.objects.filter(favorites_id=json_data.get('id'),
                                           user_id=request.user.id).exists():
            return http.HttpResponse(status=400,
                                     content_type='application/json')
        else:
            # Подсчитываем сколько раз рецепт был добавлен в избранное
            count_recipe_favorites(json_data)

            FavoritesRecipes.objects.create(favorites_id=json_data.get('id'),
                                            user_id=request.user.id)
            return JsonResponse({'success': True})
    return http.HttpResponse(status=405, content_type='application/json')


def remove_favorite_recipe(request, recipe_id):
    if request.method == 'DELETE':
        if FavoritesRecipes.objects.filter(favorites_id=recipe_id,
                                           user_id=request.user.id).exists():
            FavoritesRecipes.objects.filter(favorites_id=recipe_id,
                                            user_id=request.user.id).delete()
            return JsonResponse({'success': True})
        else:
            return http.HttpResponse(status=400,
                                     content_type='application/json')
    return http.HttpResponse(status=405, content_type='application/json')


def parse_ingredients(request):
    query = request.GET.get('query', [])
    ingredients_query = Ingredient.objects.filter(
        title__istartswith=query
    ).values('title', 'dimension')

    response = [ingredient for ingredient in ingredients_query]
    return JsonResponse(response, safe=False)
