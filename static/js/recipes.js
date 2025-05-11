import { getRecipes } from './api.js';

document.addEventListener('DOMContentLoaded', () => {
    const recipeGrid = document.getElementById('recipeGrid');
    const searchInput = document.getElementById('searchInput');

    // Load recipes
    loadRecipes();

    // Search functionality
    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const query = searchInput.value.trim();
                if (query) {
                    loadRecipes(query);
                }
            }
        });
    }

    async function loadRecipes(query = '') {
        try {
            const recipes = await getRecipes(query);
            displayRecipes(recipes);
        } catch (error) {
            console.error('Error loading recipes:', error);
            showError('Failed to load recipes');
        }
    }

    function displayRecipes(recipes) {
        if (!recipeGrid) return;

        recipeGrid.innerHTML = '';

        if (recipes.length === 0) {
            recipeGrid.innerHTML = `
                <div class="no-recipes">
                    <p>No recipes found</p>
                </div>
            `;
            return;
        }

        recipes.forEach(recipe => {
            const recipeCard = createRecipeCard(recipe);
            recipeGrid.appendChild(recipeCard);
        });
    }

    function createRecipeCard(recipe) {
        const card = document.createElement('div');
        card.className = 'recipe-card';
        card.innerHTML = `
            <img src="${recipe.image_url}" alt="${recipe.title}" class="recipe-image">
            <div class="recipe-info">
                <h3>${recipe.title}</h3>
                <p class="publisher">By ${recipe.publisher.publisher_name}</p>
                <div class="recipe-meta">
                    <span><i class="fas fa-clock"></i> ${recipe.cooking_time} mins</span>
                    <span><i class="fas fa-star"></i> ${recipe.social_rank}</span>
                </div>
                <a href="/recipe/${recipe.id}" class="view-recipe-btn">View Recipe</a>
            </div>
        `;
        return card;
    }

    function showError(message) {
        if (!recipeGrid) return;

        recipeGrid.innerHTML = `
            <div class="error-message">
                <p>${message}</p>
                <button onclick="loadRecipes()" class="retry-button">Retry</button>
            </div>
        `;
    }
}); 