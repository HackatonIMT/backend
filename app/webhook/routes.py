from flask import Blueprint, jsonify, request
from app import inscription_session

webhook_route = Blueprint('webhook', __name__)


@webhook_route.route('/webhook', methods=['POST'])
def webhook():

    req = request.get_json(force=True)
    print(request)
    print("\n##############################\n")
    print(req)
    action = req.get('queryResult').get('action')
    print('action ' + action)
    intention = req.get('queryResult').get('intent').get('displayName')

    reponse = {
        "fulfillmentText": u"Désolé, mais je ne sais pas encore répondre à l'intention: " + intention
    }
    if action == "testWebhook":
        # construction de la réponse

        response_text = "Ok webhook"

        reponse = {
            "fulfillmentText": response_text
        }
    # elif action == "choix1.intersemestreinscriptioncreationchoix1-selectnumber.intersemestreinscriptioncreationchoix2-selectnumber.intersemestreinscriptioncreationchoix3-selectnumber":
    elif action == "choix1":
        id = req.get("originalDetectIntentRequest").get("payload").get("data").get("sender").get("id")
        inscription_session[id] = {"choices": [int(req.get('queryResult').get('parameters').get('number')[0])]}
    elif action in ["choix2", "choix3", "choix4"]:
        id = req.get("originalDetectIntentRequest").get("payload").get("data").get("sender").get("id")
        inscription_session[id]["choices"].append(int(req.get('queryResult').get('parameters').get('number')[0]))
        reponse = {}
    elif action == "inscription.nom":
        id = req.get("originalDetectIntentRequest").get("payload").get("data").get("sender").get("id")
        inscription_session[id]["name"] = req.get('queryResult').get('parameters').get('person')

        response_text = "C'est bien ! Votre inscription :\n{}\nVos choix des cours en ordre de priorité : {}, {}, {} et {}.\n\nConfirmer l'inscription ?"
        reponse = {
            "fulfillmentText": response_text.format(inscription_session[id]["name"], *inscription_session[id]["choices"])
        }
    else:
        reponse = {}

    return jsonify(reponse)
