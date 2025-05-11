import { logout } from './api.js';

document.addEventListener('DOMContentLoaded', () => {
    const searchToggle = document.querySelector('.search-toggle');
    const searchInput = document.querySelector('.nav-search-input');
    const logoutBtn = document.getElementById('logoutBtn');
    const userProfile = document.querySelector('.user-profile');

    // Search toggle functionality
    if (searchToggle && searchInput) {
        searchToggle.addEventListener('click', () => {
            searchInput.classList.toggle('active');
            if (searchInput.classList.contains('active')) {
                searchInput.focus();
            }
        });

        searchInput.addEventListener('blur', () => {
            if (!searchInput.value) {
                searchInput.classList.remove('active');
            }
        });
    }

    // Logout functionality
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            try {
                await logout();
                window.location.href = '/login';
            } catch (error) {
                console.error('Logout error:', error);
            }
        });
    }

    // Profile dropdown functionality
    if (userProfile) {
        const profilePicture = userProfile.querySelector('.profile-picture');
        const dropdown = userProfile.querySelector('.profile-dropdown');

        profilePicture.addEventListener('click', () => {
            dropdown.classList.toggle('active');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!userProfile.contains(e.target)) {
                dropdown.classList.remove('active');
            }
        });
    }

    // Search functionality
    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const query = searchInput.value.trim();
                if (query) {
                    window.location.href = `/?search=${encodeURIComponent(query)}`;
                }
            }
        });
    }
}); 