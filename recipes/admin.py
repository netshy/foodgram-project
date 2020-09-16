from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple

from .models import Recipe, Tag, SubscriptionsUsers, RecipeIngredient, \
    Ingredient, FavoritesRecipes, ShoppingList


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'counter', 'created')
    search_fields = ('name', 'author')
    readonly_fields = ('counter', 'created')
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
