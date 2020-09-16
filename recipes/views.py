from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.views.generic import CreateView, UpdateView

from recipes.forms import RecipeCreateOrUpdateForm
from recipes.models import Recipe, User, SubscriptionsUsers, \
    FavoritesRecipes, ShoppingList, Tag


def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def index(request):
    recipes_list = Recipe.objects.select_related(
        'author'
    ).prefetch_related(
        'tag',
    )

    # Проверяем фильтрацию по тегам
    if 'filters' in request.GET:
        filters = request.GET.getlist('filters')
        recipes_list = Recipe.objects.filter(
            tag__slug__in=filters).distinct()

    all_tags = Tag.objects.all()

    paginator = Paginator(recipes_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page': page,
        'paginator': paginator,
        'all_tags': all_tags,
    }

    return render(request, 'index.html', context=context)


def authors_recipes(request, username):
    author = get_object_or_404(User, username=username)

    recipes = Recipe.objects.select_related().filter(author_id=author.pk)

    # Проверяем фильтрацию по тегам
    if 'filters' in request.GET:
        filters = request.GET.getlist('filters')
        recipes = recipes.filter(
            tag__slug__in=filters).distinct()

    all_tags = Tag.objects.all()

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page': page,
        'paginator': paginator,
        'author': author,
        'all_tags': all_tags
    }

    return render(request, 'authors_recipes.html', context=context)


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = recipe.recipe_ingredients.select_related().all()

    context = {
        'recipe': recipe,
        'ingredients': ingredients
    }
    return render(request, 'recipe_detail.html', context=context)


@login_required
def favorites(request):
    user = get_object_or_404(User, username=request.user)
    favorites_recipes = FavoritesRecipes.objects.prefetch_related(
        'favorites__tag', 'favorites__author'
    ).filter(
        user=user)

    # Проверяем фильтрацию по тегам
    if 'filters' in request.GET:
        filters = request.GET.getlist('filters')
        favorites_recipes = favorites_recipes.filter(
            favorites__tag__slug__in=filters).distinct()

    all_tags = Tag.objects.all()

    paginator = Paginator(favorites_recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page': page,
        'paginator': paginator,
        'all_tags': all_tags,

    }
    return render(request, 'favorites.html', context=context)


@login_required
def shopping_list(request):
    recipe_shopping_list = ShoppingList.objects.select_related(
        'recipe'
    ).filter(
        user=request.user.id
    )

    context = {
        'shopping_list': recipe_shopping_list,
    }
    return render(request, 'shopping-list.html', context=context)


@login_required
def my_followings(request):
    following = SubscriptionsUsers.objects.select_related(
        'user', 'author'
    ).filter(
        user=request.user
    )

    paginator = Paginator(following, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {

        'page': page,
        'paginator': paginator,

    }

    return render(request, 'my-following.html', context=context)


def download_shopping_list(request):
    recipes = Recipe.objects.filter(shoppinglist__user=request.user)
    ingredients = recipes.values(
        'ingredients__title', 'ingredients__dimension'
    ).annotate(
        Sum('recipeingredient__amount'))

    content = ''

    for item in ingredients:
        right_position_item = item.get('ingredients__title'), \
                              str(item.get('recipeingredient__amount__sum')), \
                              item.get('ingredients__dimension')
        content += ' '.join(right_position_item) + '\n'

    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=shopping-list.txt'
    return response


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeCreateOrUpdateForm
    success_url = '/'
    template_name = 'recipe-new.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeCreateOrUpdateForm
    success_url = '/'
    template_name = 'recipe-edit.html'

    def get_object(self, queryset=None):
        recipe_id = self.kwargs.get('recipe_id')
        if Recipe.objects.filter(pk=recipe_id,
                                 author=self.request.user).exists():
            return get_object_or_404(Recipe, pk=recipe_id)
        return redirect('/')  # не работает
