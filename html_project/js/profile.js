document.addEventListener('DOMContentLoaded', () => {
    // Check if user is authenticated
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
        return;
    }

    const profileForm = document.getElementById('profileForm');
    const profileImage = document.getElementById('profileImage');
    const changeImageBtn = document.getElementById('changeImageBtn');
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/*';

    // Load user profile data
    loadUserProfile();

    // Handle profile form submission
    profileForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const newPassword = document.getElementById('newPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        const currentPassword = document.getElementById('currentPassword').value;

        // Validate passwords if changing
        if (newPassword || confirmPassword || currentPassword) {
            if (!currentPassword) {
                showNotification('Please enter your current password', 'error');
                return;
            }
            if (newPassword !== confirmPassword) {
                showNotification('New passwords do not match', 'error');
                return;
            }
            if (newPassword.length < 4) {
                showNotification('New password must be at least 4 characters', 'error');
                return;
            }
        }

        const formData = {
            name: document.getElementById('name').value,
            username: document.getElementById('username').value,
            email: document.getElementById('email').value,
            currentPassword: currentPassword || undefined,
            newPassword: newPassword || undefined
        };

        try {
            const response = await updateProfile(formData);
            if (response.success) {
                showNotification('Profile updated successfully!', 'success');
                // Update navbar profile info
                updateNavbarProfile(response.user);
                // Clear password fields
                document.getElementById('currentPassword').value = '';
                document.getElementById('newPassword').value = '';
                document.getElementById('confirmPassword').value = '';
            } else {
                showNotification(response.message || 'Failed to update profile', 'error');
            }
        } catch (error) {
            showNotification('An error occurred while updating profile', 'error');
            console.error('Profile update error:', error);
        }
    });

    // Handle profile image change
    changeImageBtn.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (file) {
            try {
                const formData = new FormData();
                formData.append('profileImage', file);

                const response = await updateProfileImage(formData);
                if (response.success) {
                    profileImage.src = response.imageUrl;
                    // Update navbar profile picture
                    updateNavbarProfilePicture(response.imageUrl);
                    showNotification('Profile picture updated successfully!', 'success');
                } else {
                    showNotification(response.message || 'Failed to update profile picture', 'error');
                }
            } catch (error) {
                showNotification('An error occurred while updating profile picture', 'error');
                console.error('Profile image update error:', error);
            }
        }
    });

    // Handle logout
    document.getElementById('logoutBtn').addEventListener('click', async (e) => {
        e.preventDefault();
        try {
            await logout();
            window.location.href = 'login.html';
        } catch (error) {
            console.error('Logout error:', error);
            showNotification('An error occurred while logging out', 'error');
        }
    });
});

async function loadUserProfile() {
    try {
        const user = await getCurrentUser();
        if (user) {
            // Populate form fields
            document.getElementById('name').value = user.name || '';
            document.getElementById('username').value = user.username || '';
            document.getElementById('email').value = user.email || '';
            document.getElementById('role').value = user.role_name || 'user';
            
            // Set profile image
            const profileImage = document.getElementById('profileImage');
            profileImage.src = user.profile_picture || '../assets/default-profile.png';
            
            // Update navbar profile info
            updateNavbarProfile(user);
        } else {
            window.location.href = 'login.html';
        }
    } catch (error) {
        console.error('Error loading user profile:', error);
        showNotification('Failed to load user profile', 'error');
    }
}

function updateNavbarProfile(user) {
    const navbarProfile = document.querySelector('.user-profile');
    if (navbarProfile) {
        const profilePicture = navbarProfile.querySelector('.profile-picture');
        const username = navbarProfile.querySelector('.username');
        
        if (profilePicture) {
            profilePicture.src = user.profile_picture || '../assets/default-profile.png';
        }
        if (username) {
            username.textContent = user.name || user.username;
        }
    }
}

function updateNavbarProfilePicture(imageUrl) {
    const profilePicture = document.querySelector('.user-profile .profile-picture');
    if (profilePicture) {
        profilePicture.src = imageUrl;
    }
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    // Add to document
    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Add notification styles
const style = document.createElement('style');
style.textContent = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 2rem;
        border-radius: 5px;
        color: white;
        font-weight: 500;
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    }

    .notification.success {
        background-color: #28a745;
    }

    .notification.error {
        background-color: #dc3545;
    }

    .notification.info {
        background-color: #17a2b8;
    }

    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style); 