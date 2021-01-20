from flask import Blueprint, jsonify
from app import dialogflow

dialogflow_route = Blueprint('dialogflow', __name__)


@dialogflow_route.route('/intents', methods=['GET'])
def get_intents():
    intents = dialogflow.get_intents()
    output_data = [{'id': intent.name.split('/')[-1], 'name': intent.name, 'display_name': intent.display_name} for intent in intents]
    return jsonify(output_data), 200


@dialogflow_route.route('/intents/<intent_id>', methods=['GET'])
def get_intent(intent_id):
    intent = dialogflow.get_intent(intent_id)
    messages = []
    training_phrases = []
    for message in intent.messages:
        messages += list(message.text.text)
    for training_phrase in intent.training_phrases:
        training_phrases += list(training_phrase.text.text)
    output_data = {
        "name": intent.name,
        "display_name": intent.display_name,
        "training_phrases": training_phrases,
        "messages": messages,
        "action": intent.action,
        "priority": intent.priority,
    }  # TODO: add more data
    return jsonify(output_data), 200


@dialogflow_route.route('/intents/<intent_id>', methods=['DELETE'])
def delete_intent(intent_id):
    dialogflow.delete_intent(intent_id)
    return '', 204
