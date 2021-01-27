from app import app
from app.user.routes import user_route
from app.dialogflow.routes import dialogflow_route
from app.webhook.routes import webhook_route


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


app.register_blueprint(user_route)
app.register_blueprint(dialogflow_route)
app.register_blueprint(webhook_route)
