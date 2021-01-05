from flask import Blueprint, jsonify

user_route = Blueprint('user', __name__)


@user_route.route('/user/<user_id>', methods=['GET'])
def get_carousel(user_id):
    # TODO: replace it with a class and a request to the database (only if we need a user in the project)
    print(user_id)
    return jsonify({'full_name': 'Helder Betiol'}), 200
