from flask import Flask
from flask_cors import CORS
from app.dialogflow.dialogflow import Dialogflow

app = Flask(__name__)
CORS(app)

dialogflow = Dialogflow()

from app import routes
