from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Recipe, User, Publisher, RecipeMethod

def home(request):
    recipes = Recipe.objects.all().order_by('-social_rank')
    return render(request, 'index.html', {'recipes': recipes})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.name = request.POST.get('name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        if request.POST.get('new_password'):
            user.set_password(request.POST.get('new_password'))
        user.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('profile')
    return render(request, 'profile.html')

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, recipe_id=recipe_id)
    return render(request, 'recipe-detail.html', {'recipe': recipe})

@login_required
def add_recipe(request):
    if request.method == 'POST':
        publisher = Publisher.objects.create(
            publisher_name=request.POST.get('publisher_name'),
            publisher_url=request.POST.get('publisher_url')
        )
        recipe = Recipe.objects.create(
            title=request.POST.get('title'),
            source_url=request.POST.get('source_url'),
            social_rank=float(request.POST.get('social_rank', 0)),
            image_url=request.POST.get('image_url'),
            recipe_id=request.POST.get('recipe_id'),
            publisher=publisher,
            created_by=request.user
        )
        methods = request.POST.get('recipe_method', '').split('\n')
        for i, method in enumerate(methods, 1):
            if method.strip():
                RecipeMethod.objects.create(
                    recipe=recipe,
                    step_number=i,
                    instruction=method.strip()
                )
        messages.success(request, 'Recipe added successfully')
        return redirect('recipe_detail', recipe_id=recipe.recipe_id)
    return render(request, 'add-recipe.html')
