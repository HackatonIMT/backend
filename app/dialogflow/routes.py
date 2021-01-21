from flask import Blueprint, jsonify, request
from app import dialogflow
from app.dialogflow.models import Intent

dialogflow_route = Blueprint('dialogflow', __name__)


# DialogFlow has a bug in which it does not send the training phrases. For this, we obtain them from the database

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
    if not training_phrases:
        aux_intent = Intent.objects(dialogflow_id=intent_id).first()
        if aux_intent:
            training_phrases = aux_intent.training_phrases
    output_data = {
        "id": intent.name.split('/')[-1],
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
    intent = Intent.objects(dialogflow_id=intent_id)
    intent.delete()
    return '', 204


@dialogflow_route.route('/intents', methods=['POST'])
def create_intent():
    input_data = request.get_json()
    intent = dialogflow.create_intent(input_data.get('display_name'), input_data.get('training_phrases'), input_data.get('messages'))
    Intent.save_from_dialogflow_intent(intent, input_data.get('training_phrases'))
    messages = []
    training_phrases = []
    for message in intent.messages:
        messages += list(message.text.text)
    for training_phrase in intent.training_phrases:
        for part in training_phrase.parts:
            training_phrases.append(part.text)
    output_data = {
        "id": intent.name.split('/')[-1],
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
        "id": intent.name.split('/')[-1],
        "name": intent.name,
        "display_name": intent.display_name,
        "training_phrases": training_phrases,
        "messages": messages,
        "action": intent.action,
        "priority": intent.priority,
    }  # TODO: add more data
    return jsonify(output_data), 200


@dialogflow_route.route('/fix', methods=['GET'])
def fix_training_phrases():
    intents = {"0cdff40f-5126-4c99-9903-013c038a869a": ["25", "1", "le deuxième", "le premier et le deuxième", "choisis le premier et le deuxième",
                                                        "je choisis le numéro 3", "numéros 4, 5, 7 et 8", "choisis les numéros 1, 2, 3 et 5",
                                                        "choisis le premier", "je choisis le numéro 2 et le numéro 5", "voir 1, 2, 3, 4 et 5"],
               "fb7e5c89-18d8-46f6-bcd3-40b75e009eee": ["salutations", "rebonjour", "bonjour à toi", "re bonjour", "allo", "coucou",
                                                        "hey", "hé", "resalut", "salut", "re salut", "salut à tous", "bonjour"],
               "53655751-142b-4cee-870d-54361e798b7a": ["aurais-je forcément mon premier choix ?", "est ce que j'aurai automatiquement mon premier choix ?",
                                                        "l'affectation à un sujet est elle définitive ?", "Pouvons nous changer de sujet après l'inscription ?",
                                                        "comment serons nous affectés aux sujets ?", "Suis-je obligé d'assister à l'intersemestre meme si le sujet ne m'interesse pas ?",
                                                        "Comment se feront les affectations?"],
               "a95ca5ee-6815-4c00-a27c-4b3245423589": ["Quelles compétences seront évaluées pendant l'intersemestre ?", "comment est évalué l'intersemestre ?",
                                                        "Quelles compétences vais-je obtenir ?"],
               "14858e10-896f-49f8-984d-9581921ab203": ["J'ai des questions sur l'intersemestre", "Ou trouvez des infos sur l'intersemestre ?",
                                                        "Qui contacter pour avoir des informations sur l'intersemestre ?"],
               "d82b4517-c92a-4bdc-9b48-acc835c3d6c9": ["Quand auront lieu les intersemestres 2021 ?", "A quelles dates auront lieu les intersemestres 2021 ?"],
               "0e301baa-6d5f-4e37-8832-104ffedac554": ["Sous quel format se feront les intersemestres ?", "Quel sera le format des sujets de l'intersemestre ?",
                                                        "Sous quel format seront dispensés les sujets ?"],
               "64eb2808-b611-482e-b64e-865e0da62330": ["25", "1", "le deuxième", "le premier et le deuxième", "choisis le premier et le deuxième",
                                                        "je choisis le numéro 3", "numéros 4, 5, 7 et 8", "choisis les numéros 1, 2, 3 et 5",
                                                        "choisis le premier", "je choisis le numéro 2 et le numéro 5", "voir 1, 2, 3, 4 et 5"],
               "d25138c7-bb50-42b9-9aa4-8f1ff3ef29b3": ["Je veux m'inscrire", "Je veux m'inscrire. Je suis en 2ème année FISE sur le campus de Brest."],
               "0dc7ae62-4d11-4c49-8169-7f93432826c0": ["25", "1", "le deuxième", "le premier et le deuxième", "choisis le premier et le deuxième",
                                                        "je choisis le numéro 3", "numéros 4, 5, 7 et 8", "choisis les numéros 1, 2, 3 et 5",
                                                        "choisis le premier", "je choisis le numéro 2 et le numéro 5", "voir 1, 2, 3, 4 et 5"],
               "d16efd75-3788-45b1-b0ee-1cc023ec0e53": ["25", "1", "le deuxième", "le premier et le deuxième", "choisis le premier et le deuxième",
                                                        "je choisis le numéro 3", "numéros 4, 5, 7 et 8", "choisis les numéros 1, 2, 3 et 5",
                                                        "choisis le premier", "je choisis le numéro 2 et le numéro 5", "voir 1, 2, 3, 4 et 5"],
               "76c0a611-8fec-4cbf-af9b-889f2c2b6102": ["LEGOFF Lucas"],
               "60def3fa-07ed-4a31-afe8-3bf258c47f86": ["je ne crois pas", "ça ne m'intéresse pas", "ne le fais pas", "pas vraiment", "sûrement pas",
                                                        "non merci", "je n'en veux pas", "je ne suis pas d'accord", "non"],
               "86f2f8cc-5c14-4536-ae94-738ad0297883": ["yes", "fais-le", "c'est correct", "d'accord", "bien sûr", "exactement",
                                                        "confirmer", "je suis d'accord", "oui", "ça me va"],
               "db7c9c22-4536-4bba-98ce-af98a4b670e4": ["comment puis je m'inscrire à l'intersemetre ?", "comment s'inscrire ?"],
               "2388c892-7602-44f2-8cab-5410af097d1d": ["dans quelle langue se fera l'intersemetre ?", "est ce que je dois avoir un niveau particulier en français pour participer à l'intersemestre ?",
                                                        "il y a t il des niveaux langues requis pour l'intersemestre ?"],
               "0da99116-4505-44da-9bb8-bbbdf26f66fb": ["Ou aura lieu l'intersemestre ?", "l'intersemestre se fera t il à distance cette année ?",
                                                        "Est-il possible d'assister en présentiel à un sujet d'intersemestre en 2021 ?"],
               "7a87604a-23dc-43d1-a890-37baef46c34d": ["Quels sont les cours ?", "Quels sont les sujets de l'intersemestre ?",
                                                        "Ou puis je trouver la liste des sujets pour l'intersemestre ?"],

               }

    for key, value in intents.items():
        intent = Intent.objects(dialogflow_id=key).first()
        if intent is None:
            print(f"{key} is Null")
            continue
        intent.update(training_phrases=value)
    return 'ok'
