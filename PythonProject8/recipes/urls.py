from django.urls import path
from . import views

app_name = "recipes"

urlpatterns = [
    path("", views.recipe_list, name="list"),
    path("search/", views.search, name="search"),
    path("stats/", views.stats, name="stats"),
    path("random/", views.random_recipe, name="random"),
    path("category/<str:cat_name>/", views.category_detail, name="category"),
    path("<int:pk>/", views.recipe_detail, name="detail"),
]