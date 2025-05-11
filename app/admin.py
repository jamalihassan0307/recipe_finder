from django.contrib import admin
from .models import Role, User, Publisher, Recipe, RecipeMethod

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'role_name')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role')
    list_filter = ('role',)
    search_fields = ('username', 'email')

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('id', 'publisher_name', 'publisher_url')
    search_fields = ('publisher_name',)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'publisher', 'social_rank', 'created_by')
    list_filter = ('publisher', 'created_by')
    search_fields = ('title', 'recipe_id')

@admin.register(RecipeMethod)
class RecipeMethodAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'step_number')
    list_filter = ('recipe',)
    ordering = ('recipe', 'step_number')
