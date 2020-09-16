from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('recipes/<int:recipe_id>/', views.recipe_detail,
         name='recipe_detail'),
    path('recipes/new/', views.RecipeCreateView.as_view(), name='new-recipe'),
    path('recipes/<int:recipe_id>/edit/', views.RecipeUpdateView.as_view(),
         name='recipe-edit'),

    path('favorites/', views.favorites, name='favorites'),
    path('shopping-list/', views.shopping_list, name='shopping-list'),
    path('shopping-list/download-list/', views.download_shopping_list,
         name='print_shopping_list'),
    path('my_followings/', views.my_followings, name='my_followings'),

    path('<str:username>/', views.authors_recipes, name='authors-recipes'),
    path('', views.index, name='index'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
