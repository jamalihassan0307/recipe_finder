from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Recipe, User, Publisher, RecipeMethod
from django.db.models import Q
from django.http import HttpResponse

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
                created_by=request.user
            )

            # Create recipe methods
            methods = request.POST.get('recipe_methods', '').split('\n')
            for i, method in enumerate(methods, 1):
                if method.strip():
                    RecipeMethod.objects.create(
                        recipe=recipe,
                        step_number=i,
                        description=method.strip()
                    )

            messages.success(request, 'Recipe added successfully!')
            return redirect('recipe_detail', recipe_id=recipe.id)
        except Exception as e:
            messages.error(request, f'Error adding recipe: {str(e)}')
            return redirect('add_recipe')

    return render(request, 'add-recipe.html')

def load_recipe(request):
    # Hardcoded recipe data
    recipes_data = [
        {
            "image_url": "https://th.bing.com/th/id/OIP.3qzGOXJXldbpC7QIfJUaTQAAAA?rs=1&pid=ImgDetMain",
            "publisher": "101 Cookbooks",
            "publisher_url": "http://www.101cookbooks.com",
            "recipe_id": "47746",
            "social_rank": 1000,
            "source_url": "http://www.101cookbooks.com/archives/001199.html",
            "title": "Best Pizza awais",
            "recipe_method": "Mix flour,buttol, water, yeast, and salt. Let it rise for 1-2 hours. Roll out and bake.",
            "id": "053019bb901e88187361"
        },
        {
            "image_url": "http://forkify-api.herokuapp.com/images/fruitpizza9a19.jpg",
            "publisher": "The Pioneer Woman",
            "publisher_url": "http://thepioneerwoman.com",
            "recipe_id": "46956",
            "social_rank": 10000,
            "source_url": "http://thepioneerwoman.com/cooking/2012/01/fruit-pizza/",
            "title": "Deep Dish Fruit Pizza",
            "recipe_method": "Prepare a cookie crust. Top with cream cheese frosting and assorted fresh fruits.",
            "id": "44c63d98e1992976ad7a"
        },
        {
            "image_url": "http://forkify-api.herokuapp.com/images/Pizza2BDip2B12B500c4c0a26c.jpg",
            "publisher": "Closet Cooking",
            "publisher_url": "http://closetcooking.com",
            "recipe_id": "35477",
            "social_rank": 99.99999999999994,
            "source_url": "http://www.closetcooking.com/2011/03/pizza-dip.html",
            "title": "Pizza Dip",
            "recipe_method": "Layer pizza sauce, cheese, and your favorite toppings in a baking dish. Bake until golden and bubbly.",
            "id": "a87b2728a110a7d91b63"
        },
        {
            "id": 3,
            "image_url": "http://forkify-api.herokuapp.com/images/BBQChickenPizzawithCauliflowerCrust5004699695624ce.jpg",
            "publisher": "Closet Cooking",
            "publisher_url": "http://closetcooking.com",
            "recipe_id": "41470",
            "social_rank": 99.9999999999994,
            "source_url": "http://www.closetcooking.com/2013/02/cauliflower-pizza-crust-with-bbq.html",
            "title": "Cauliflower Pizza Crust (with BBQ Chicken Pizza)",
            "recipe_method": "Make a cauliflower crust, top with BBQ chicken, cheese, and bake until crisp."
        },
        {
            "image_url": "http://forkify-api.herokuapp.com/images/Pizza2BQuesadillas2B2528aka2BPizzadillas25292B5002B834037bf306b.jpg",
            "publisher": "Closet Cooking",
            "publisher_url": "http://closetcooking.com",
            "recipe_id": "35478",
            "social_rank": 99.99999999999835,
            "source_url": "http://www.closetcooking.com/2012/11/pizza-quesadillas-aka-pizzadillas.html",
            "title": "Pizza Quesadillas (aka Pizzadillas)",
            "recipe_method": "Fill tortillas with pizza ingredients, fold them, and cook in a pan until crispy.",
            "id": "f005d171875ad10ed6ed"
        },
        {
            "image_url": "http://forkify-api.herokuapp.com/images/sweetpotatokalepizza2c6db.jpg",
            "publisher": "Two Peas and Their Pod",
            "publisher_url": "http://www.twopeasandtheirpod.com",
            "recipe_id": "54454",
            "social_rank": 99.9999999991673,
            "source_url": "http://www.twopeasandtheirpod.com/sweet-potato-kale-pizza-with-rosemary-red-onion/",
            "title": "Sweet Potato Kale Pizza with Rosemary & Red Onion",
            "recipe_method": "Roast sweet potato slices, layer with kale, rosemary, and red onions. Bake on pizza dough.",
            "id": "bfcfa777be092440ea54"
        },
        {
            "image_url": "http://forkify-api.herokuapp.com/images/PizzaDip21of14f05.jpg",
            "publisher": "My Baking Addiction",
            "publisher_url": "http://www.mybakingaddiction.com",
            "recipe_id": "2ec050",
            "social_rank": 99.99999999826605,
            "source_url": "http://www.mybakingaddiction.com/pizza-dip/",
            "title": "Pizza Dip",
            "recipe_method": "Mix pizza sauce, cheese, and toppings. Bake in a dish until bubbly and serve with chips.",
            "id": "39d0372856e234453757"
        },
        {
            "image_url": "http://forkify-api.herokuapp.com/images/pizza3464.jpg",
            "publisher": "The Pioneer wonder Woman",
            "publisher_url": "http://thepioneerwoman.com",
            "recipe_id": "6fab1",
            "social_rank": 99,
            "source_url": "http://thepioneerwoman.com/cooking/2013/04/pizza-potato-skins/",
            "title": "Pizza Potato Skins",
            "recipe_method": "Bake potato skins, then top with pizza sauce, cheese, and other pizza toppings.",
            "id": "6f6ef1982ead424fe130"
        },
        {
            "image_url": "http://forkify-api.herokuapp.com/images/pizza292x2007a259a79.jpg",
            "publisher": "Simply Recipes",
            "publisher_url": "http://simplyrecipes.com",
            "recipe_id": "36453",
            "social_rank": 80.06,
            "source_url": "http://www.simplyrecipes.com/recipes/homemade_pizza/",
            "title": "Homemade Pizza",
            "recipe_method": "Make your dough from scratch, add your toppings, and bake at a high temperature for a crispy crust.",
            "id": "fe45cfeb928f5ecb8d97"
        },
        {
            "image_url": "https://th.bing.com/th/id/OIP.fDWEOEHk6trKCevpKK8-LgHaEO?rs=1&pid=ImgDetMain",
            "publisher": "Biryani Huut",
            "publisher_url": "http://simplyrecipes.com",
            "social_rank": 100,
            "source_url": " https://www.foodfusion.com ",
            "title": "Biryani",
            "recipe_method": "rice chicken onion green chli tomato",
            "recipe_id": "36453",
            "id": "2"
        }
    ]

    created_count = 0
    for data in recipes_data:
        # 1. Create or get Publisher
        publisher, _ = Publisher.objects.get_or_create(
            publisher_name=data["publisher"],
            defaults={"publisher_url": data.get("publisher_url", "")}
        )
        # 2. Avoid duplicate recipes by recipe_id
        if not Recipe.objects.filter(recipe_id=data["recipe_id"]).exists():
            # 3. Create Recipe (without saving yet, so we can add methods after)
            recipe = Recipe(
                title=data["title"],
                description=data.get("recipe_method", ""),
                image_url=data["image_url"],
                source_url=data["source_url"].strip(),
                social_rank=data["social_rank"],
                publisher=publisher,
                recipe_id=data["recipe_id"],
                cooking_time=30,  # Default value, adjust as needed
                created_by=None  # Or set to a user if needed
            )
            recipe.save()
            # 4. Create RecipeMethod (at least one, from recipe_method field)
            method_text = data.get("recipe_method", "")
            if method_text:
                RecipeMethod.objects.create(
                    recipe=recipe,
                    step_number=1,
                    description=method_text
                )
            created_count += 1
    return HttpResponse(f"DATA LOAD SUCCESS: {created_count} recipes added.")
