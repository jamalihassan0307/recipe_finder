import { login } from './api.js';

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.querySelector('.login-form');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const email = emailInput.value.trim();
        const password = passwordInput.value;

        if (!email || !password) {
            showError('Please fill in all fields');
            return;
        }

        try {
            const response = await login(email, password);
            if (response.success) {
                window.location.href = '/';
            } else {
                showError(response.message || 'Login failed');
            }
        } catch (error) {
            showError('An error occurred during login');
            console.error('Login error:', error);
        }
    });

    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'alert alert-danger';
        errorDiv.textContent = message;

        const existingError = document.querySelector('.alert');
        if (existingError) {
            existingError.remove();
        }

        loginForm.insertBefore(errorDiv, loginForm.firstChild);
    }
}); 