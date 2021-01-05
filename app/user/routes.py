from flask import Blueprint, jsonify

user_route = Blueprint('user', __name__)


@user_route.route('/user', methods=['GET'])
def get_carousel():
    # TODO: replace it with a class and a request to the database (only if we need a user in the project)
    return jsonify({'full_name': 'Helder Betiol'}), 200
