from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/update-picture/', views.update_profile_picture, name='update_profile_picture'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<int:recipe_id>/save/', views.save_recipe, name='save_recipe'),
    path('add-recipe/', views.add_recipe, name='add_recipe'),
    
    # Admin routes - updated paths
    path('recipe/publisher/add/', views.add_publisher, name='add_publisher'),
    path('recipe/manage/', views.manage_recipes, name='manage_recipes'),
    path('recipe/<int:recipe_id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipe/<int:recipe_id>/delete/', views.delete_recipe, name='delete_recipe'),
    path('social-auth/', include('social_django.urls', namespace='social')),

]
 