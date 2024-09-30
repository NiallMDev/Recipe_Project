from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe
from django.http import HttpResponse
from django.http import JsonResponse


# API View to return all recipes in JSON format
def api_recipes(request):
    recipes = Recipe.objects.all().values('id', 'recipe_name', 'recipe_description', 'recipe_image')
    return JsonResponse(list(recipes), safe=False)

def recipes(request):
    if request.method == 'POST':
        data = request.POST
        recipe_image = request.FILES.get('recipe_image')
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')

        Recipe.objects.create(
            recipe_image=recipe_image,
            recipe_name=recipe_name,
            recipe_description=recipe_description,
        )
        return redirect('/')

    queryset = Recipe.objects.all()

    if request.GET.get('search'):
        queryset = queryset.filter(
            recipe_name__icontains=request.GET.get('search'))

    context = {'recipes': queryset}
    return render(request, 'recipe/recipes.html', context)

def delete_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    recipe.delete()
    return redirect('recipe_list')


def update_recipe(request, id):
    queryset = Recipe.objects.get(id=id)

    if request.method == 'POST':
        data = request.POST
        recipe_image = request.FILES.get('recipe_image')
        recipe_name = data.get('recipe_name')
        recipe_description = data.get('recipe_description')

        queryset.recipe_name = recipe_name
        queryset.recipe_description = recipe_description

        if recipe_image:
            queryset.recipe_image = recipe_image

        queryset.save()
        return redirect('/')
    
    context = {'recipe': queryset}
    return render(request, 'recipe/update_recipe.html', context)
