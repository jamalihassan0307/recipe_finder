document.addEventListener('DOMContentLoaded', () => {
    updateNavbarState();
});

function updateNavbarState() {
    const user = getCurrentUser();
    const navLinks = document.querySelector('.nav-links');
    const loginButton = navLinks.querySelector('.login-button');
    const userProfile = navLinks.querySelector('.user-profile');

    if (user && user.isAuthenticated) {
        // Show user profile, hide login button
        if (loginButton) loginButton.style.display = 'none';
        
        // Create user profile if it doesn't exist
        if (!userProfile) {
            const profileHTML = `
                <div class="user-profile">
                    <img src="${user.profileImage}" alt="Profile" class="profile-picture">
                    <span class="username">${user.name}</span>
                    <div class="profile-dropdown">
                        <a href="profile.html" class="dropdown-item">
                            <i class="fas fa-user"></i> Profile
                        </a>
                        <a href="#" class="dropdown-item" id="logoutBtn">
                            <i class="fas fa-sign-out-alt"></i> Logout
                        </a>
                    </div>
                </div>
            `;
            navLinks.insertAdjacentHTML('beforeend', profileHTML);

            // Add logout event listener
            document.getElementById('logoutBtn').addEventListener('click', (e) => {
                e.preventDefault();
                logout();
            });
        } else {
            // Update existing user profile
            const profilePicture = userProfile.querySelector('.profile-picture');
            const username = userProfile.querySelector('.username');
            
            if (profilePicture) profilePicture.src = user.profileImage;
            if (username) username.textContent = user.name;
        }
    } else {
        // Show login button, hide user profile
        if (loginButton) loginButton.style.display = 'flex';
        if (userProfile) userProfile.remove();
    }
} 