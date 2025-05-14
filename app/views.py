from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Recipe, User, Publisher, RecipeMethod
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

def home(request):
    search_query = request.GET.get('search', '')
    filter_type = request.GET.get('filter', '')
    
    recipes = Recipe.objects.select_related('publisher').all()
    
    # Apply search filter if exists
    if search_query:
        recipes = recipes.filter(
            Q(title__icontains=search_query) |
            Q(publisher__publisher_name__icontains=search_query)
        )
    
    # Apply category filters
    if filter_type:
        if filter_type == 'popular':
            recipes = recipes.order_by('-social_rank')
        elif filter_type == 'recent':
            recipes = recipes.order_by('-created_at')
        elif filter_type == 'trending':
            # Get recipes from the last 7 days with highest social rank
            week_ago = timezone.now() - timedelta(days=7)
            recipes = recipes.filter(created_at__gte=week_ago).order_by('-social_rank')
        elif filter_type == 'vegetarian':
            recipes = recipes.filter(is_vegetarian=True)
        elif filter_type == 'vegan':
            recipes = recipes.filter(is_vegan=True)
        elif filter_type == 'gluten-free':
            recipes = recipes.filter(is_gluten_free=True)
    else:
        # Default sorting by social rank
        recipes = recipes.order_by('-social_rank')
    
    return render(request, 'index.html', {
        'recipes': recipes,
        'current_filter': filter_type,
        'search_query': search_query
    })

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        # Handle contact form submission
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('contact')
    return render(request, 'contact.html')

def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=identifier, password=password)
        if user is None:
            # Try to find user by email
            try:
                user_obj = User.objects.get(email=identifier)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email/username or password.')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('login')

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, 'Profile updated successfully!')
    return redirect('profile')

@login_required
def update_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        user = request.user
        user.profile_picture = request.FILES['profile_picture']
        user.save()
        messages.success(request, 'Profile picture updated successfully!')
    return redirect('profile')

@login_required
def change_password(request):
    if request.method == 'POST':
        user = request.user
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
        else:
            try:
                validate_password(new_password, user)
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password changed successfully!')
            except ValidationError as e:
                messages.error(request, e.messages[0])
    
    return redirect('profile')

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe.objects.select_related('publisher', 'created_by').prefetch_related('methods'), id=recipe_id)
    methods = recipe.methods.all()
    return render(request, 'recipe-detail.html', {'recipe': recipe, 'methods': methods})

@login_required
def save_recipe(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = request.user
        if recipe in user.saved_recipes.all():
            user.saved_recipes.remove(recipe)
            messages.success(request, 'Recipe removed from saved recipes.')
        else:
            user.saved_recipes.add(recipe)
            messages.success(request, 'Recipe saved successfully!')
    return redirect('recipe_detail', recipe_id=recipe_id)

@login_required
def add_recipe(request):
    if request.method == 'POST':
        try:
            # Create or get publisher
            publisher_name = request.POST.get('publisher_name')
            publisher_url = request.POST.get('publisher_url')
            publisher, created = Publisher.objects.get_or_create(
                publisher_name=publisher_name,
                defaults={'publisher_url': publisher_url}
            )

            # Create recipe
            recipe = Recipe.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                source_url=request.POST.get('source_url'),
                image_url=request.POST.get('image_url'),
                cooking_time=int(request.POST.get('cooking_time', 0)),
                social_rank=float(request.POST.get('social_rank', 0)),
                publisher=publisher,
                created_by=request.user,
                is_vegetarian=request.POST.get('is_vegetarian') == 'on',
                is_vegan=request.POST.get('is_vegan') == 'on',
                is_gluten_free=request.POST.get('is_gluten_free') == 'on'
            )

            # Create recipe methods
            methods = request.POST.get('recipe_methods', '').split('\n')
            for i, method in enumerate(methods, 1):
                if method.strip():
                    RecipeMethod.objects.create(
                        recipe=recipe,
                        step_number=i,
                        instruction=method.strip()
                    )

            messages.success(request, 'Recipe added successfully!')
            return redirect('recipe_detail', recipe_id=recipe.id)
        except Exception as e:
            messages.error(request, f'Error adding recipe: {str(e)}')
            return redirect('add_recipe')

    return render(request, 'add-recipe.html')
