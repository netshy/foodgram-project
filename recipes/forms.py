from django import forms

from recipes.models import Recipe, Tag, Ingredient, RecipeIngredient


class RecipeCreateOrUpdateForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        to_field_name='slug'
    )
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        to_field_name='title'
    )
    amount = []

    class Meta:
        model = Recipe
        fields = ('name', 'tags', 'ingredients', 'cooking_time', 'description',
                  'image')

        #  https://docs.djangoproject.com/en/3.1/ref/request-response/#django.http.QueryDict.update

    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy()

            for tag in ('breakfast', 'lunch', 'dinner'):
                if tag in data:
                    data.update({'tags': tag})

            for item in list(data):
                if item.startswith('nameIngredient_'):
                    data.update({'ingredients': data.get(item)})
                elif item.startswith('valueIngredient_'):
                    self.amount.append(data.get(item))

        super().__init__(data=data, *args, **kwargs)

    def save(self, commit=True):
        recipe_obj = super().save(commit=False)

        # Сохраняю поля, кроме ingredients и tags
        recipe_obj.save()

        #  Это для случая, когда редактируешь рецепт,
        #  старые ингредиенты не дублировались.
        #  Они сначала удаляются, а потом записываются новые всем скопом.
        recipe_obj.recipe_ingredients.all().delete()

        # Записываем в связанную сущность RecipeIngredient - ингредиенты
        ingredients_amount = self.amount
        recipe_obj.recipe_ingredients.set(
            [
                RecipeIngredient(recipe=recipe_obj, ingredient=ingredient,
                                 amount=abs(int(amount)))
                for ingredient, amount in
                zip(self.cleaned_data['ingredients'], ingredients_amount)
            ],
            bulk=False)

        # Записываем в связанную сущность Tag_Recipe - теги
        recipe_obj.tag.set([tag for tag in self.cleaned_data['tags']])

        self.save_m2m()
        return recipe_obj
