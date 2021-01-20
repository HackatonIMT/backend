from app import app
from app.user.routes import user_route
from app.weather.routes import weather_route
from app.dialogflow.routes import dialogflow_route


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


app.register_blueprint(user_route)
app.register_blueprint(weather_route)
app.register_blueprint(dialogflow_route)
