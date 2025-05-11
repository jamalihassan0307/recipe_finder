// API endpoints
const API_ENDPOINTS = {
    RECIPES: '/api/recipes/',
    RECIPE_DETAIL: (id) => `/api/recipes/${id}/`,
    LOGIN: '/api/login/',
    LOGOUT: '/api/logout/',
    PROFILE: '/api/profile/',
    UPDATE_PROFILE: '/api/profile/update/',
    CHANGE_PASSWORD: '/api/profile/change-password/',
};

// API request helper
async function apiRequest(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        credentials: 'include',
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(endpoint, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
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

// Recipe API functions
export async function getRecipes() {
    return apiRequest(API_ENDPOINTS.RECIPES);
}

export async function getRecipeDetail(id) {
    return apiRequest(API_ENDPOINTS.RECIPE_DETAIL(id));
}

// Authentication API functions
export async function login(email, password) {
    return apiRequest(API_ENDPOINTS.LOGIN, 'POST', { email, password });
}

export async function logout() {
    return apiRequest(API_ENDPOINTS.LOGOUT, 'POST');
}

// Profile API functions
export async function getProfile() {
    return apiRequest(API_ENDPOINTS.PROFILE);
}

export async function updateProfile(data) {
    return apiRequest(API_ENDPOINTS.UPDATE_PROFILE, 'PUT', data);
}

export async function changePassword(currentPassword, newPassword) {
    return apiRequest(API_ENDPOINTS.CHANGE_PASSWORD, 'POST', {
        current_password: currentPassword,
        new_password: newPassword,
    });
} 