#!/usr/bin/python3
'''Module to set up endpoint for Amenity object'''
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    users = storage.all(User).values()
    # list of dict (from obj to dict)
    users_list = [user.to_dict() for user in users]

    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    if 'email' not in request_data:
        abort(400, 'Missing email')
    if 'password' not in request_data:
        abort(400, 'Missing password')
    new_user = User(**request_data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in request_data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
