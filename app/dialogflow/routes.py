from flask import Blueprint, jsonify
from app import dialogflow

dialogflow_route = Blueprint('dialogflow', __name__)


@dialogflow_route.route('/intents', methods=['GET'])
def get_intents():
    intents = dialogflow.get_intents()

    return jsonify(intents), 200
