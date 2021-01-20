from flask import Blueprint, jsonify, request

webhook_route = Blueprint('webhook', __name__)


@webhook_route.route('/webhook', methods=['POST'])
def webhook():

    req = request.get_json(force=True)
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

    return jsonify(reponse)
