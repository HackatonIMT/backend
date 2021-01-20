from flask import Flask
from flask_cors import CORS
import os
from google.cloud import dialogflow_v2

app = Flask(__name__)
CORS(app)


intents_client = dialogflow_v2.IntentsClient()
intents_parent = dialogflow_v2.AgentsClient.agent_path(os.environ["PROJECT_ID"])

from app import routes
