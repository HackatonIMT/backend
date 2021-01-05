from app import app
from app.user.routes import user_route


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


app.register_blueprint(user_route)
