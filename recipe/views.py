from django.shortcuts import get_object_or_404, render
from django.db.models import Count
import random

from .models import Recipe, Category


def main(request):
    all_recipes = list(Recipe.objects.all())
    random_recipes = random.sample(all_recipes, min(10, len(all_recipes)))
    return render(request, 'main.html', {'recipes': random_recipes})


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    recipes = Recipe.objects.filter(category=category)
    return render(request, 'category_detail.html', {
        'category': category,
        'recipes': recipes,
    })
