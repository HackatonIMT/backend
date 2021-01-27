from google.cloud import dialogflow_v2
from google.protobuf import field_mask_pb2
import os
from google.oauth2 import service_account

from app.dialogflow.models import Intent


class Dialogflow:
    def __init__(self):
        credentials_aux = {
          "type": "service_account",
          "project_id": os.environ["PROJECT_ID"],
          "private_key_id": os.environ["PRIVATE_KEY_ID"],
          "private_key": os.environ["PRIVATE_KEY"].replace('\\n', '\n'),
          "client_email": os.environ["CLIENT_EMAIL"],
          "client_id": os.environ["CLIENT_ID"],
          "auth_uri": "https://accounts.google.com/o/oauth2/auth",
          "token_uri": "https://oauth2.googleapis.com/token",
          "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
          "client_x509_cert_url": os.environ["CLIENT_CERT"]
        }
        print(f"\nMY PRINT: {os.environ['PROJECT_ID']}\n")
        credentials = service_account.Credentials.from_service_account_info(credentials_aux)

        self.intents_client = dialogflow_v2.IntentsClient(credentials=credentials)
        self.intents_parent = dialogflow_v2.AgentsClient(credentials=credentials).agent_path(os.environ["PROJECT_ID"])

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

    def update_intent(self, original_intent, display_name, training_phrases_parts, message_texts):
        """Create an intent of the given intent type."""
        old_intent = Intent.objects(dialogflow_id=original_intent.name.split('/')[-1]).first()
        updated_paths = []
        if display_name:
            original_intent.display_name = display_name
            updated_paths.append('display_name')
            old_intent.display_name = display_name
        if training_phrases_parts:
            training_phrases = []
            training_phrases_parts = old_intent.training_phrases + training_phrases_parts  # TODO: get old training phrase from database (Dialogflow is not returning them)
            for training_phrases_part in training_phrases_parts:
                part = dialogflow_v2.Intent.TrainingPhrase.Part(text=training_phrases_part)
                # Here we create a new training phrase for each provided part.
                training_phrase = dialogflow_v2.Intent.TrainingPhrase(parts=[part])
                training_phrases.append(training_phrase)
            original_intent.training_phrases = training_phrases
            updated_paths.append('training_phrases')
            old_intent.training_phrases = training_phrases_parts

        if message_texts:
            messages = []
            for message in original_intent.messages:
                messages += list(message.text.text)
            messages += message_texts
            text = dialogflow_v2.Intent.Message.Text(text=messages)
            message = dialogflow_v2.Intent.Message(text=text)
            original_intent.messages = [message]
            updated_paths.append('messages')
            old_intent.messages = [messages]

        update_mask = field_mask_pb2.FieldMask(paths=updated_paths)
        response = self.intents_client.update_intent(intent=original_intent, language_code='fr', update_mask=update_mask)
        old_intent.save()
        return response

    def delete_message(self, original_intent, message_id):
        old_intent = Intent.objects(dialogflow_id=original_intent.name.split('/')[-1]).first()
        messages = []
        for message in original_intent.messages:
            messages += list(message.text.text)
        print(messages)
        print(message_id)

        messages.pop(message_id)
        text = dialogflow_v2.Intent.Message.Text(text=messages)
        message = dialogflow_v2.Intent.Message(text=text)
        original_intent.messages = [message]
        old_intent.messages = [messages]
        update_mask = field_mask_pb2.FieldMask(paths=["messages"])
        response = self.intents_client.update_intent(intent=original_intent, language_code='fr', update_mask=update_mask)
        old_intent.save()
        return response

    def delete_training_phrase(self, original_intent, phrase_id):
        old_intent = Intent.objects(dialogflow_id=original_intent.name.split('/')[-1]).first()

        training_phrases = []
        training_phrases_parts = old_intent.training_phrases
        print(training_phrases_parts)
        print(phrase_id)
        training_phrases_parts.pop(phrase_id)
        for training_phrases_part in training_phrases_parts:
            part = dialogflow_v2.Intent.TrainingPhrase.Part(text=training_phrases_part)
            # Here we create a new training phrase for each provided part.
            training_phrase = dialogflow_v2.Intent.TrainingPhrase(parts=[part])
            training_phrases.append(training_phrase)
        original_intent.training_phrases = training_phrases
        old_intent.training_phrases = training_phrases_parts

        update_mask = field_mask_pb2.FieldMask(paths=["training_phrases"])
        response = self.intents_client.update_intent(intent=original_intent, language_code='fr', update_mask=update_mask)
        old_intent.save()
        return response
