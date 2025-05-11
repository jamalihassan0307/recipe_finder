from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Recipe, User, Publisher, RecipeMethod
from django.db.models import Q

def home(request):
    search_query = request.GET.get('search', '')
    recipes = Recipe.objects.all()
    
    if search_query:
        recipes = recipes.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(publisher__publisher_name__icontains=search_query)
        )
    
    recipes = recipes.order_by('-social_rank')
    return render(request, 'index.html', {'recipes': recipes})

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
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
    
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
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipe-detail.html', {'recipe': recipe})

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
