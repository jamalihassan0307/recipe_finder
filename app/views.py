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
from functools import wraps
import os
from django.templatetags.static import static

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.role.role_name == 'admin':
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

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
    # The profile_picture_url is already handled by the User model's property
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
        try:
            user = request.user
            # Delete old profile picture if it exists
            if user.profile_picture and os.path.isfile(user.profile_picture.path):
                os.remove(user.profile_picture.path)
            
            # Save new profile picture
            user.profile_picture = request.FILES['profile_picture']
            user.save()
            messages.success(request, 'Profile picture updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating profile picture: {str(e)}')
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
    methods = recipe.methods.all().order_by('step_number')
    is_admin = request.user.is_authenticated and request.user.role.role_name == 'admin'
    
    return render(request, 'recipe-detail.html', {
        'recipe': recipe,
        'methods': methods,
        'is_admin': is_admin
    })

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
            # Get publisher from selection
            publisher_id = request.POST.get('publisher')
            publisher = get_object_or_404(Publisher, id=publisher_id)

            # Create recipe
            recipe = Recipe.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                source_url=request.POST.get('source_url', ''),
                image_url=request.POST.get('image_url'),
                cooking_time=int(request.POST.get('cooking_time', 0)),
                social_rank=float(request.POST.get('social_rank', 0)),
                publisher=publisher,
                created_by=request.user,
                is_vegetarian=request.POST.get('is_vegetarian') == 'on',
                is_vegan=request.POST.get('is_vegan') == 'on',
                is_gluten_free=request.POST.get('is_gluten_free') == 'on'
            )

            # Create recipe methods from dynamic steps
            methods = request.POST.getlist('method[]')
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

    publishers = Publisher.objects.all()
    return render(request, 'add-recipe.html', {'publishers': publishers})

@login_required
@admin_required
def add_publisher(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            name = request.POST.get('publisher_name')
            url = request.POST.get('publisher_url')
            
            if Publisher.objects.filter(publisher_name=name).exists():
                messages.error(request, 'A publisher with this name already exists.')
            else:
                Publisher.objects.create(
                    publisher_name=name,
                    publisher_url=url
                )
                messages.success(request, 'Publisher added successfully!')
                
        elif action == 'edit':
            publisher_id = request.POST.get('publisher_id')
            name = request.POST.get('publisher_name')
            url = request.POST.get('publisher_url')
            
            try:
                publisher = Publisher.objects.get(id=publisher_id)
                if Publisher.objects.filter(publisher_name=name).exclude(id=publisher_id).exists():
                    messages.error(request, 'A publisher with this name already exists.')
                else:
                    publisher.publisher_name = name
                    publisher.publisher_url = url
                    publisher.save()
                    messages.success(request, 'Publisher updated successfully!')
            except Publisher.DoesNotExist:
                messages.error(request, 'Publisher not found.')
                
        elif action == 'delete':
            publisher_id = request.POST.get('publisher_id')
            try:
                publisher = Publisher.objects.get(id=publisher_id)
                # Check if there are any recipes associated with this publisher
                if Recipe.objects.filter(publisher=publisher).exists():
                    messages.error(request, 'Cannot delete publisher with associated recipes. Please delete or reassign the recipes first.')
                else:
                    publisher.delete()
                    messages.success(request, 'Publisher deleted successfully!')
            except Publisher.DoesNotExist:
                messages.error(request, 'Publisher not found.')
                
        return redirect('add_publisher')
        
    publishers = Publisher.objects.all()
    return render(request, 'add-publisher.html', {'publishers': publishers})

@login_required
@admin_required
def manage_recipes(request):
    recipes = Recipe.objects.select_related('publisher', 'created_by').all()
    return render(request, 'manage-recipes.html', {'recipes': recipes})

@login_required
@admin_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    publishers = Publisher.objects.all()
    methods = recipe.methods.all().order_by('step_number')
    
    if request.method == 'POST':
        try:
            # Update publisher
            publisher_id = request.POST.get('publisher')
            publisher = get_object_or_404(Publisher, id=publisher_id)
            
            # Update recipe
            recipe.title = request.POST.get('title')
            recipe.description = request.POST.get('description')
            recipe.source_url = request.POST.get('source_url')
            recipe.image_url = request.POST.get('image_url')
            recipe.cooking_time = int(request.POST.get('cooking_time', 0))
            recipe.social_rank = float(request.POST.get('social_rank', 0))
            recipe.publisher = publisher
            recipe.is_vegetarian = request.POST.get('is_vegetarian') == 'on'
            recipe.is_vegan = request.POST.get('is_vegan') == 'on'
            recipe.is_gluten_free = request.POST.get('is_gluten_free') == 'on'
            recipe.save()
            
            # Update methods
            recipe.methods.all().delete()
            methods = request.POST.get('recipe_methods', '').split('\n')
            for i, method in enumerate(methods, 1):
                if method.strip():
                    RecipeMethod.objects.create(
                        recipe=recipe,
                        step_number=i,
                        instruction=method.strip()
                    )
            
            messages.success(request, 'Recipe updated successfully!')
            return redirect('recipe_detail', recipe_id=recipe.id)
            
        except Exception as e:
            messages.error(request, f'Error updating recipe: {str(e)}')
            
    return render(request, 'edit-recipe.html', {
        'recipe': recipe,
        'publishers': publishers,
        'methods': methods
    })

@login_required
@admin_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Recipe deleted successfully!')
        return redirect('manage_recipes')
    return render(request, 'delete-recipe-confirm.html', {'recipe': recipe})

