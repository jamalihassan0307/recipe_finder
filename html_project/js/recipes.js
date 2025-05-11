document.addEventListener('DOMContentLoaded', () => {
    const recipesGrid = document.getElementById('recipesGrid');
    const searchInput = document.querySelector('.nav-search-input');
    const filterTags = document.querySelectorAll('.filter-tag');
    let recipes = [];
    let activeFilter = 'all';

    // Load recipes
    async function loadRecipes() {
        try {
            recipes = await getRecipes();
            renderRecipes();
        } catch (error) {
            console.error('Error loading recipes:', error);
            recipesGrid.innerHTML = '<div class="error-message">Failed to load recipes. Please try again later.</div>';
        }
    }

    // Render recipes
    function renderRecipes() {
        let filteredRecipes = [...recipes];

        // Apply search filter
        if (searchInput.value) {
            const searchTerm = searchInput.value.toLowerCase();
            filteredRecipes = filteredRecipes.filter(recipe => 
                recipe.title.toLowerCase().includes(searchTerm) ||
                recipe.publisher.toLowerCase().includes(searchTerm)
            );
        }

        // Apply category filter
        switch (activeFilter) {
            case 'popular':
                filteredRecipes = filteredRecipes.sort((a, b) => b.social_rank - a.social_rank).slice(0, 10);
                break;
            case 'recent':
                filteredRecipes = filteredRecipes.slice(-10).reverse();
                break;
            case 'trending':
                filteredRecipes = filteredRecipes
                    .sort((a, b) => {
                        const rankWeight = 0.7;
                        const recentWeight = 0.3;
                        const rankScore = (b.social_rank - a.social_rank) * rankWeight;
                        const recentScore = (b.id - a.id) * recentWeight;
                        return rankScore + recentScore;
                    })
                    .slice(0, 10);
                break;
        }

        if (filteredRecipes.length === 0) {
            recipesGrid.innerHTML = '<div class="no-results">No recipes found</div>';
            return;
        }

        recipesGrid.innerHTML = filteredRecipes.map(recipe => `
            <div class="recipe-card">
                <div class="recipe-image-container">
                    <img src="${recipe.image_url}" alt="${recipe.title}">
                    <div class="recipe-overlay">
                        <span class="social-rank">
                            ⭐ ${Math.round(recipe.social_rank)}
                        </span>
                    </div>
                </div>
                <div class="recipe-content">
                    <h3>${recipe.title}</h3>
                    <p class="publisher">By ${recipe.publisher}</p>
                    <div class="recipe-card-actions">
                        <a href="${recipe.source_url}" target="_blank" rel="noopener noreferrer" class="view-recipe-btn">
                            View Recipe
                        </a>
                        <button onclick="window.location.href='recipe-detail.html?id=${recipe.recipe_id}'" class="view-details-btn">
                            View Details
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    }

    // Search functionality
    searchInput.addEventListener('input', renderRecipes);

    // Filter functionality
    filterTags.forEach(tag => {
        tag.addEventListener('click', () => {
            filterTags.forEach(t => t.classList.remove('active'));
            tag.classList.add('active');
            activeFilter = tag.textContent.toLowerCase();
            renderRecipes();
        });
    });

    // Search toggle
    const searchToggle = document.querySelector('.search-toggle');
    searchToggle.addEventListener('click', () => {
        searchInput.style.display = searchInput.style.display === 'none' ? 'block' : 'none';
        if (searchInput.style.display === 'block') {
            searchInput.focus();
        }
    });

    // Initial load
    loadRecipes();
}); 