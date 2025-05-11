from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    role_name = models.CharField(max_length=100)

    def __str__(self):
        return self.role_name

class User(AbstractUser):
    profile_picture = models.CharField(max_length=255, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.username

class Publisher(models.Model):
    publisher_name = models.CharField(max_length=100)
    publisher_url = models.CharField(max_length=255)

    def __str__(self):
        return self.publisher_name

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    source_url = models.CharField(max_length=255)
    social_rank = models.FloatField()
    image_url = models.CharField(max_length=255)
    recipe_id = models.CharField(max_length=100)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class RecipeMethod(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='methods')
    step_number = models.IntegerField()
    instruction = models.TextField()

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f"{self.recipe.title} - Step {self.step_number}"
