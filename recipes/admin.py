from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.forms import CheckboxSelectMultiple

from recipes.models import (Recipe, Tag, SubscriptionsUsers, RecipeIngredient,
                            Ingredient, FavoritesRecipes, ShoppingList)
from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    def count_favorites_recipes_now(self, obj):
        return obj.favoritesrecipes_set.count()

    count_favorites_recipes_now.short_description = 'Counter favorites recipes'

    list_display = ('name', 'author', 'created')
    search_fields = ('name', 'author')
    readonly_fields = ('count_favorites_recipes_now', 'created')
    empty_value_display = '-пусто-'
    list_filter = ('author', 'name', 'tag')
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    inlines = (RecipeIngredientInline,)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'dimension')
    search_fields = ('title',)
    list_filter = ('title',)
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(SubscriptionsUsers)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk',)
    empty_value_display = '-пусто-'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk',)
    empty_value_display = '-пусто-'


@admin.register(FavoritesRecipes)
class FavoritesRecipesAdmin(admin.ModelAdmin):
    list_display = ('pk',)
    empty_value_display = '-пусто-'


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('pk',)
    empty_value_display = '-пусто-'
