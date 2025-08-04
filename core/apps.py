from django.apps import AppConfig
import cloudinary
import os
from dotenv import load_dotenv

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    def ready(self):
        load_dotenv()
        cloudinary.config( 
            cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'), 
            api_key = os.getenv('CLOUDINARY_API_KEY'), 
            api_secret = os.getenv('CLOUDINARY_API_SECRET') 
        )