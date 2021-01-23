import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    MONGODB_SETTINGS = {
        'host': os.environ.get('MONGO_DATABASE_URL'),
    }

    CREDENTIALS = {
          "type": "service_account",
          "project_id": os.environ["PROJECT_ID"],
          "private_key_id": os.environ["PRIVATE_KEY_ID"],
          "private_key": os.environ["PRIVATE_KEY"],
          "client_email": "haackathonchatbot@hackathonchatbot-dkyq.iam.gserviceaccount.com",
          "client_id": os.environ["CLIENT_ID"],
          "auth_uri": "https://accounts.google.com/o/oauth2/auth",
          "token_uri": "https://oauth2.googleapis.com/token",
          "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
          "client_x509_cert_url": os.environ["CLIENT_CERT"]
    }
