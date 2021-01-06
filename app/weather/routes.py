from flask import Blueprint, jsonify, request
import requests
import os

owmtoken = os.environ['OWM_TOKEN']
owmurl = "http://api.openweathermap.org/data/2.5/"


weather_route = Blueprint('weather', __name__)


@weather_route.route('/weather', methods=['POST'])
def get_weather():
    data = request.get_json(force=True)
    city = data.get('city')
    if not city:
        return '', 404
    url = f"{owmurl}weather/?q={city}&lang=fr&APPID={owmtoken}"
    output = requests.get(url)
    if output.status_code >= 400:
        return '', 404
    result = output.json()
    return jsonify({'description': result['weather'][0]["description"],
                    'tempMax': result['main']['temp_max'] - 273.15,
                    'tempMin': result['main']['temp_min'] - 273.15}), 200
