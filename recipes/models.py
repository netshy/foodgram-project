from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False


class Ingredient(models.Model):
    title = models.CharField(max_length=255, db_index=True,  unique=True)
    dimension = models.CharField(max_length=20, db_index=True)

    def __str__(self):
        return f'Ingredient name: {self.title}, dimension {self.dimension}'


class Tag(models.Model):
    name = models.CharField(max_length=10, null=True)
    slug = models.SlugField(max_length=10, null=True, unique=True)
    color = models.CharField(verbose_name='check box style', max_length=10,
                             null=True)

    def __str__(self):
        return f'Tag: {self.name}'


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='recipe name',
        max_length=255,
        db_index=True
    )
    author = models.ForeignKey(
        User,
        verbose_name='authors recipe',
        on_delete=models.CASCADE,
        related_name='author_user',
        db_index=True
    )
    description = models.TextField(verbose_name='recipe description')
    cooking_time = models.IntegerField()
    image = models.ImageField(upload_to='recipe')
    created = models.DateTimeField(verbose_name='time publication',
                                   auto_now=True)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient'
    )
    tag = models.ManyToManyField(
        Tag,
        related_name='recipe_tag',
    )
    counter = models.PositiveIntegerField(
        verbose_name='counting the number of subscriptions', editable=False,
        default=0)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Recipe name: {self.name}, author: {self.author}'

    def is_favorite(self, user_id):
        response = FavoritesRecipes.objects.filter(
            user=user_id, favorites=self.id
        ).exists()
        return response

    def is_in_cart(self, user_id):
        response = ShoppingList.objects.filter(
            user=user_id, recipe=self.id
        ).exists()
        return response

    def split_description(self):
        return self.description.split('\n')


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_ingredients',
        on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    amount = models.IntegerField()


class SubscriptionsUsers(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        unique_together = ['user', 'author']

    def __str__(self):
        return f'User: {self.user}, author: {self.author}'

    def is_following(self, author_id):
        response = SubscriptionsUsers.objects.select_related(
            'user', 'author'
        ).filter(
            user=self.id, author=author_id
        ).exists()
        return response


class FavoritesRecipes(models.Model):
    favorites = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ['user', 'favorites']

    def __str__(self):
        return f'User: {self.user}, favorite recipe: {self.favorites.name}'


class ShoppingList(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ['user', 'recipe']

    def __str__(self):
        return f'User: {self.user}, recipe_id: {self.recipe.id}'
