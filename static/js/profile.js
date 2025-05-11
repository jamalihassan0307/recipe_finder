import { updateProfile, changePassword } from './api.js';

document.addEventListener('DOMContentLoaded', () => {
    const profileForm = document.querySelector('.profile-form');
    const passwordForm = document.querySelector('.password-form');
    const avatarInput = document.getElementById('avatarInput');
    const profilePicture = document.getElementById('profilePicture');

    // Profile update functionality
    if (profileForm) {
        profileForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const formData = new FormData(profileForm);
            const data = {
                username: formData.get('username'),
                email: formData.get('email'),
            };

            try {
                const response = await updateProfile(data);
                if (response.success) {
                    showMessage('Profile updated successfully', 'success');
                } else {
                    showMessage(response.message || 'Failed to update profile', 'error');
                }
            } catch (error) {
                showMessage('An error occurred while updating profile', 'error');
                console.error('Profile update error:', error);
            }
        });
    }

    // Password change functionality
    if (passwordForm) {
        passwordForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const formData = new FormData(passwordForm);
            const currentPassword = formData.get('current_password');
            const newPassword = formData.get('new_password');
            const confirmPassword = formData.get('confirm_password');

            if (newPassword !== confirmPassword) {
                showMessage('New passwords do not match', 'error');
                return;
            }

            try {
                const response = await changePassword(currentPassword, newPassword);
                if (response.success) {
                    showMessage('Password changed successfully', 'success');
                    passwordForm.reset();
                } else {
                    showMessage(response.message || 'Failed to change password', 'error');
                }
            } catch (error) {
                showMessage('An error occurred while changing password', 'error');
                console.error('Password change error:', error);
            }
        });
    }

    // Profile picture upload functionality
    if (avatarInput && profilePicture) {
        avatarInput.addEventListener('change', async (e) => {
            const file = e.target.files[0];
            if (!file) return;

            const formData = new FormData();
            formData.append('profile_picture', file);

            try {
                const response = await updateProfile(formData);
                if (response.success) {
                    profilePicture.src = URL.createObjectURL(file);
                    showMessage('Profile picture updated successfully', 'success');
                } else {
                    showMessage(response.message || 'Failed to update profile picture', 'error');
                }
            } catch (error) {
                showMessage('An error occurred while updating profile picture', 'error');
                console.error('Profile picture update error:', error);
            }
        });
    }

    function showMessage(message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `alert alert-${type}`;
        messageDiv.textContent = message;

        const existingMessage = document.querySelector('.alert');
        if (existingMessage) {
            existingMessage.remove();
        }

        document.querySelector('.profile-container').insertBefore(
            messageDiv,
            document.querySelector('.profile-content')
        );

        setTimeout(() => {
            messageDiv.remove();
        }, 5000);
    }
}); 