const API_URL = 'https://677801d980a79bf91903a685.mockapi.io/api';
const ENDPOINTS = {
    RECIPES: "/recipe",
    PROFILE: "/users"
};

async function getRecipes() {
    try {
        const response = await fetch(`${API_URL}${ENDPOINTS.RECIPES}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return Array.isArray(data) ? data : [];
    } catch (error) {
        console.error('Error fetching recipes:', error);
        throw new Error('Failed to fetch recipes. Please try again later.');
    }
}

async function getRecipeById(id) {
    try {
        const response = await fetch(`${API_URL}${ENDPOINTS.RECIPES}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        const recipe = data.find(r => r.recipe_id === id);
        if (!recipe) {
            throw new Error('Recipe not found');
        }
        return recipe;
    } catch (error) {
        console.error('Error fetching recipe:', error);
        throw new Error(error.message || 'Failed to fetch recipe. Please try again later.');
    }
}

async function addRecipe(recipe) {
    try {
        const response = await fetch(`${API_URL}${ENDPOINTS.RECIPES}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(recipe),
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error adding recipe:', error);
        throw new Error('Failed to add recipe. Please try again later.');
    }
}

async function updateRecipe(id, recipe) {
    try {
        const response = await fetch(`${API_URL}${ENDPOINTS.RECIPES}/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(recipe),
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error updating recipe:', error);
        throw new Error('Failed to update recipe. Please try again later.');
    }
}

async function deleteRecipe(id) {
    try {
        const response = await fetch(`${API_URL}${ENDPOINTS.RECIPES}/${id}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return true;
    } catch (error) {
        console.error('Error deleting recipe:', error);
        throw new Error('Failed to delete recipe. Please try again later.');
    }
}

async function login(email, password) {
    try {
        const response = await fetch(`${API_URL}${ENDPOINTS.PROFILE}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const users = await response.json();
        const user = users.find(u => u.email === email && u.password === password);
        if (user) {
            // Store user data in localStorage
            const userData = {
                id: user.id,
                email: user.email,
                name: user.name || email.split('@')[0],
                profileImage: user.profileImage || '../assets/default-profile.png',
                isAuthenticated: true
            };
            localStorage.setItem('user', JSON.stringify(userData));
            return userData;
        }
        throw new Error('Invalid email or password');
    } catch (error) {
        console.error('Error during login:', error);
        throw new Error(error.message || 'Failed to login. Please try again later.');
    }
}

function logout() {
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}

function getCurrentUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

function isAuthenticated() {
    return !!getCurrentUser();
}

function checkAuth() {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
    }
}

// Profile-related functions
async function updateProfile(profileData) {
    try {
        const user = getCurrentUser();
        if (!user) {
            throw new Error('User not authenticated');
        }

        const response = await fetch(`${API_URL}${ENDPOINTS.PROFILE}/${user.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
                name: profileData.name,
                username: profileData.username,
                email: profileData.email,
                password: profileData.newPassword || undefined,
                currentPassword: profileData.currentPassword || undefined
            })
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.message || 'Failed to update profile');
        }

        // Update local storage with new user data
        const updatedUser = {
            ...user,
            name: profileData.name,
            username: profileData.username,
            email: profileData.email
        };
        localStorage.setItem('user', JSON.stringify(updatedUser));

        return {
            success: true,
            user: updatedUser
        };
    } catch (error) {
        console.error('Update profile error:', error);
        throw error;
    }
}

async function updateProfileImage(formData) {
    try {
        const response = await fetch(`${API_URL}/users/profile/image`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: formData
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.message || 'Failed to update profile image');
        }

        return data;
    } catch (error) {
        console.error('Update profile image error:', error);
        throw error;
    }
} 