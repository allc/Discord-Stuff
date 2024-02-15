from dotenv import load_dotenv
from os import getenv
import secrets

load_dotenv()

DEBUG = getenv('DEBUG', 'False') == 'True'
API_ENDPOINT = 'https://discord.com/api/v10'
CLIENT_ID = getenv('CLIENT_ID')
CLIENT_SECRET = getenv('CLIENT_SECRET')
REDIRECT_URI = getenv('REDIRECT_URI')
SECRET_KEY = getenv('SECRET_KEY') or secrets.token_urlsafe(16)
