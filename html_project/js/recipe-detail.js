document.addEventListener('DOMContentLoaded', async () => {
    // Get recipe ID from URL
    const urlParams = new URLSearchParams(window.location.search);
    const recipeId = urlParams.get('id');

    if (!recipeId) {
        showError('Recipe ID not found');
        return;
    }

    try {
        // Fetch recipe details
        const recipe = await getRecipeById(recipeId);
        if (!recipe) {
            throw new Error('Recipe not found');
        }

        // Update page content
        updateRecipeDetails(recipe);

    } catch (error) {
        console.error('Error loading recipe:', error);
        showError(error.message || 'Failed to load recipe details. Please try again later.');
    }
});

function updateRecipeDetails(recipe) {
    try {
        // Update basic recipe information
        document.getElementById('recipeImage').src = recipe.image_url || '../assets/default-recipe.jpg';
        document.getElementById('recipeImage').alt = recipe.title || 'Recipe Image';
        document.getElementById('recipeTitle').textContent = recipe.title || 'Untitled Recipe';
        document.getElementById('socialRank').textContent = recipe.social_rank ? Math.round(recipe.social_rank) : 'N/A';
        
        // Update publisher information
        document.getElementById('publisherName').textContent = recipe.publisher || 'Unknown Publisher';
        document.getElementById('publisherLogo').src = recipe.publisher_url || '../assets/default-publisher.jpg';
        document.getElementById('publisherLogo').alt = recipe.publisher || 'Publisher Logo';
        document.getElementById('publisherLink').href = recipe.publisher_url || '#';
        
        // Update source URL
        const sourceUrlElement = document.getElementById('sourceUrl');
        sourceUrlElement.href = recipe.source_url || '#';
        sourceUrlElement.style.display = recipe.source_url ? 'flex' : 'none';

        // Update recipe method if available
        if (recipe.recipe_method) {
            const methodContainer = document.createElement('div');
            methodContainer.className = 'info-card method-card';
            methodContainer.innerHTML = `
                <h2>Cooking Instructions</h2>
                <p>${recipe.recipe_method}</p>
            `;
            document.querySelector('.recipe-main-info').appendChild(methodContainer);
        }

        // Update ingredients
        const ingredientsGrid = document.querySelector('.ingredients-grid');
        ingredientsGrid.innerHTML = recipe.ingredients
            .slice(0, 4) // Show only first 4 ingredients
            .map(ingredient => `
                <div class="ingredient-item">
                    <span class="ingredient-icon">🥘</span>
                    <span>${ingredient}</span>
                </div>
            `)
            .join('');

        // Setup share buttons
        setupShareButtons(recipe);

    } catch (error) {
        console.error('Error updating recipe details:', error);
        showError('Error displaying recipe details');
    }
}

function setupShareButtons(recipe) {
    const shareButtons = document.querySelectorAll('.share-button');
    
    shareButtons.forEach(button => {
        button.addEventListener('click', () => {
            if (!recipe.source_url) {
                showError('Cannot share recipe: Source URL not available');
                return;
            }

            const platform = button.classList[1]; // facebook, twitter, or pinterest
            let shareUrl = '';
            
            switch (platform) {
                case 'facebook':
                    shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(recipe.source_url)}`;
                    break;
                case 'twitter':
                    shareUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(recipe.title)}&url=${encodeURIComponent(recipe.source_url)}`;
                    break;
                case 'pinterest':
                    shareUrl = `https://pinterest.com/pin/create/button/?url=${encodeURIComponent(recipe.source_url)}&media=${encodeURIComponent(recipe.image_url)}&description=${encodeURIComponent(recipe.title)}`;
                    break;
            }
            
            if (shareUrl) {
                window.open(shareUrl, '_blank', 'width=600,height=400');
            }
        });
    });
}

function showError(message) {
    // Create error container if it doesn't exist
    let errorContainer = document.querySelector('.error-container');
    if (!errorContainer) {
        errorContainer = document.createElement('div');
        errorContainer.className = 'error-container';
        document.querySelector('.recipe-detail-page').prepend(errorContainer);
    }

    // Update error message
    errorContainer.innerHTML = `
        <div class="error-message">
            <p>${message}</p>
            <button onclick="window.location.href='index.html'" class="action-button secondary">
                <i class="fas fa-arrow-left"></i>
                Back to Recipes
            </button>
        </div>
    `;
} 