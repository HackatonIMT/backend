from google.cloud import dialogflow_v2
import os


class Dialogflow:
    def __init__(self):
        self.intents_client = dialogflow_v2.IntentsClient()
        self.intents_parent = dialogflow_v2.AgentsClient.agent_path(os.environ["PROJECT_ID"])

    def get_intents(self):
        intents = self.intents_client.list_intents(request={'parent': self.intents_parent})
        return [intent for intent in intents]

    def get_intent(self, intent_id):
        intent_path = self.intents_client.intent_path(os.environ["PROJECT_ID"], intent_id)
        intent = self.intents_client.get_intent(request={'name': intent_path})
        return intent

    def delete_intent(self, intent_id):
        intent_path = self.intents_client.intent_path(os.environ["PROJECT_ID"], intent_id)

        self.intents_client.delete_intent(request={'name': intent_path})
