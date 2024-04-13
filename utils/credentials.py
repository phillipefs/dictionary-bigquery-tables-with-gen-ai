import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.getcwd(), 'configs', '.env'))

############################# OPENAI CREDENTIALS #############################
OPENAI_KEY = os.getenv('openai_key')
API_VERSION = os.getenv('api_version')
OPENAI_ENDPOINT = os.getenv('azure_endpoint')
MODEL_ENGINE = os.getenv('model_engine')

########################## GOOGLE CLOUD CREDENTIALS ##########################
GCLOUD_PROJECT = os.getenv('gcp_project_id')
GOOGLE_APPLICATION_CREDENTIALS = os.path.join(os.getcwd(), 'configs', 'service_account_key.json')