from flask import Blueprint, jsonify, request
from app import dialogflow
from app.dialogflow.models import Intent

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
        for part in training_phrase.parts:
            training_phrases.append(part.text)
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


@dialogflow_route.route('/intents', methods=['POST'])
def create_intent():
    input_data = request.get_json()
    intent = dialogflow.create_intent(input_data.get('display_name'), input_data.get('training_phrases'), input_data.get('messages'))
    messages = []
    training_phrases = []
    for message in intent.messages:
        messages += list(message.text.text)
    for training_phrase in intent.training_phrases:
        for part in training_phrase.parts:
            training_phrases.append(part.text)
    output_data = {
        "name": intent.name,
        "display_name": intent.display_name,
        "training_phrases": training_phrases,
        "messages": messages,
        "action": intent.action,
        "priority": intent.priority,
    }  # TODO: add more data
    return jsonify(output_data), 200


@dialogflow_route.route('/intents/<intent_id>', methods=['PUT'])
def update_intent(intent_id):
    input_data = request.get_json()
    original_intent = dialogflow.get_intent(intent_id)
    intent = dialogflow.update_intent(original_intent, input_data.get('display_name', ""),
                                      input_data.get('training_phrases', []),
                                      input_data.get('messages', []))
    messages = []
    training_phrases = []
    for message in intent.messages:
        messages += list(message.text.text)
    for training_phrase in intent.training_phrases:
        for part in training_phrase.parts:
            training_phrases.append(part.text)

    output_data = {
        "name": intent.name,
        "display_name": intent.display_name,
        "training_phrases": training_phrases,
        "messages": messages,
        "action": intent.action,
        "priority": intent.priority,
    }  # TODO: add more data
    return jsonify(output_data), 200


# @dialogflow_route.route('/fix', methods=['GET'])
# def fix_training_phrases():
#     intents = { "0cdff40f-5126-4c99-9903-013c038a869a": ["25", "1", "le deuxième", "le premier et le deuxième", "choisis le premier et le deuxième"]}
