import datetime
from app import db


class Intent(db.Document):
    meta = {'collection': 'intent',  'indexes': ['dialogflow_id']}
    dialogflow_id = db.StringField(max_length=100, unique=True, required=True)
    messages = db.ListField(db.ListField(db.StringField()))
    training_phrases = db.ListField(db.ListField(db.StringField()))
    display_name = db.StringField(max_length=250)
    action = db.StringField(max_length=250)
    priority = db.IntField()
    parameters = db.ListField(db.StringField(max_length=50))
    # name = db.StringField(max_length=250)
    # created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    # updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

    @staticmethod
    def save_from_dialogflow_intent(dialog_intent):
        intent = Intent()
        intent.dialogflow_id = dialog_intent.name.split('/')[-1]
        intent.display_name = dialog_intent.display_name
        intent.action = dialog_intent.action
        intent.priority = dialog_intent.priority
        parameters = []
        for parameter in dialog_intent.parameters:
            parameters.append(parameter.display_name)
        intent.parameters = parameters
        messages = []
        for message in dialog_intent.messages:
            messages.append(list(message.text.text))
        intent.messages = messages
        training_phrases = []
        for training_phrase in dialog_intent.training_phrases:
            for part in training_phrase.parts:
                training_phrases.append(part.text)
        intent.training_phrases = training_phrases
        intent.save()
