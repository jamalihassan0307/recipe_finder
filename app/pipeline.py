from urllib.request import urlopen
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import os

def get_avatar(backend, strategy, details, response, user=None, *args, **kwargs):
    if backend.name == 'google-oauth2':
        if user and response.get('picture'):
            # Update user's profile picture from Google
            picture_url = response.get('picture')
            if not user.profile_picture or user.profile_picture.name == '':
                try:
                    # Download the image
                    img_temp = NamedTemporaryFile(delete=True)
                    img_temp.write(urlopen(picture_url).read())
                    img_temp.flush()
                    
                    # Save the image to the user's profile
                    user.profile_picture.save(
                        f"google_avatar_{user.id}.jpg",
                        File(img_temp),
                        save=True
                    )
                except Exception as e:
                    print(f"Error downloading Google avatar: {str(e)}")

        # Update user's additional information if available
        if user and not user.first_name and not user.last_name:
            if response.get('given_name'):
                user.first_name = response.get('given_name')
            if response.get('family_name'):
                user.last_name = response.get('family_name')
            user.save()
    return None 