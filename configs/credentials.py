import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.getcwd(), 'configs', '.env'))

OPENAI_KEY = os.getenv('openai_key')
API_VERSION = os.getenv('api_version')
OPENAI_ENDPOINT = os.getenv('azure_endpoint')