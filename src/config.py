from dotenv import load_dotenv
from os import getenv

load_dotenv()

DEBUG = getenv('DEBUG', 'False') == 'True'
API_ENDPOINT = 'https://discord.com/api/v10'
CLIENT_ID = getenv('CLIENT_ID')
CLIENT_SECRET = getenv('CLIENT_SECRET')
REDIRECT_URI = getenv('REDIRECT_URI')
