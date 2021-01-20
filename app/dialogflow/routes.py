from flask import Blueprint, jsonify
from app import intents_client, intents_parent

dialogflow_route = Blueprint('dialogflow', __name__)


@dialogflow_route.route('/intents', methods=['GET'])
def get_intents():

    intents = intents_client.list_intents(request={'parent': intents_parent})
    intents = [{'name': intent.name, 'display_name': intent.display_name} for intent in intents]

    return jsonify(intents), 200
