def get_avatar(backend, strategy, details, response, user=None, *args, **kwargs):
    if backend.name == 'google-oauth2':
        if user and response.get('picture'):
            # Update user's profile picture from Google
            picture_url = response.get('picture')
            if not user.profile_picture or user.profile_picture.name == '':
                # Only update if user doesn't have a profile picture
                user.profile_picture_url = picture_url
                user.save()

        # Update user's additional information if available
        if user and not user.first_name and not user.last_name:
            if response.get('given_name'):
                user.first_name = response.get('given_name')
            if response.get('family_name'):
                user.last_name = response.get('family_name')
            user.save()
    return None 