from google.cloud import dialogflow_v2
import os


class Dialogflow:
    def __init__(self):
        self.intents_client = dialogflow_v2.IntentsClient()
        self.intents_parent = dialogflow_v2.AgentsClient.agent_path(os.environ["PROJECT_ID"])

    def get_intents(self):
        intents = self.intents_client.list_intents(request={'parent': self.intents_parent})
        return [{'name': intent.name, 'display_name': intent.display_name} for intent in intents]
