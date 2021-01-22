from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db = MongoEngine(app)

from app.dialogflow.dialogflow import Dialogflow

dialogflow = Dialogflow()

inscription_session = []

from app import routes
