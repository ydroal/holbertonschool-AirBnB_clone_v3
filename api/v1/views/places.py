#!/usr/bin/python3
'''Module to set up endpoint for Place object'''
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    # list of place objects
    places = city.places
    places_list = [place.to_dict() for place in places]
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    if 'user_id' not in request_data:
        abort(400, 'Missing user_id')
    user = storage.get(User, request_data['user_id'])
    if not user:
        abort(404)
    if 'name' not in request_data:
        abort(400, 'Missing name')
    new_place = Place(**request_data)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in request_data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
