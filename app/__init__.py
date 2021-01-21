from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from app.dialogflow.dialogflow import Dialogflow
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db = MongoEngine(app)

dialogflow = Dialogflow()

inscription_session = []

from app import routes
