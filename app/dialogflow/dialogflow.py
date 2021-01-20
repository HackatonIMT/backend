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

    def create_intent(self, display_name, training_phrases_parts, message_texts):
        """Create an intent of the given intent type."""

        training_phrases = []
        for training_phrases_part in training_phrases_parts:
            part = dialogflow_v2.Intent.TrainingPhrase.Part(text=training_phrases_part)
            # Here we create a new training phrase for each provided part.
            training_phrase = dialogflow_v2.Intent.TrainingPhrase(parts=[part])
            training_phrases.append(training_phrase)

        text = dialogflow_v2.Intent.Message.Text(text=message_texts)
        message = dialogflow_v2.Intent.Message(text=text)

        intent = dialogflow_v2.Intent(
            display_name=display_name,
            training_phrases=training_phrases,
            messages=[message]
        )

        response = self.intents_client.create_intent(request={'parent': self.intents_parent, 'intent': intent})
        return response
