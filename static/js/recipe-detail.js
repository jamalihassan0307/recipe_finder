document.addEventListener('DOMContentLoaded', () => {
    const saveRecipeBtn = document.getElementById('saveRecipe');
    const shareRecipeBtn = document.getElementById('shareRecipe');

    // Save recipe functionality
    if (saveRecipeBtn) {
        saveRecipeBtn.addEventListener('click', async () => {
            try {
                const recipeId = window.location.pathname.split('/').filter(Boolean).pop();
                const response = await fetch(`/api/recipes/${recipeId}/save/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    credentials: 'include',
                });

                const data = await response.json();
                if (data.success) {
                    showMessage('Recipe saved successfully', 'success');
                    saveRecipeBtn.classList.toggle('saved');
                } else {
                    showMessage(data.message || 'Failed to save recipe', 'error');
                }
            } catch (error) {
                showMessage('An error occurred while saving the recipe', 'error');
                console.error('Save recipe error:', error);
            }
        });
    }

    // Share recipe functionality
    if (shareRecipeBtn) {
        shareRecipeBtn.addEventListener('click', () => {
            const recipeUrl = window.location.href;
            const shareData = {
                title: document.title,
                text: 'Check out this recipe!',
                url: recipeUrl,
            };

            if (navigator.share) {
                navigator.share(shareData)
                    .catch(error => {
                        console.error('Error sharing:', error);
                        fallbackShare(recipeUrl);
                    });
            } else {
                fallbackShare(recipeUrl);
            }
        });
    }

    function fallbackShare(url) {
        const tempInput = document.createElement('input');
        tempInput.value = url;
        document.body.appendChild(tempInput);
        tempInput.select();
        document.execCommand('copy');
        document.body.removeChild(tempInput);
        showMessage('Recipe URL copied to clipboard!', 'success');
    }

    function showMessage(message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `alert alert-${type}`;
        messageDiv.textContent = message;

        const existingMessage = document.querySelector('.alert');
        if (existingMessage) {
            existingMessage.remove();
        }

        document.querySelector('.recipe-detail-container').insertBefore(
            messageDiv,
            document.querySelector('.recipe-content')
        );

        setTimeout(() => {
            messageDiv.remove();
        }, 5000);
    }

    // Get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}); 