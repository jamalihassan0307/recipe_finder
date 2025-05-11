from django.urls import path
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
] 