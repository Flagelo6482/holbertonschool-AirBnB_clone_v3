#!/usr/bin/python3
"""Places route"""
from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.user import User
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places(city_id):
    """Return json file the dictionary of all places"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)

    lis = []
    for i in storage.all(Place).values():
        if i.city_id == city_id:
            lis.append(i.to_dict())

    return jsonify(lis)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def places_id(place_id):
    """Return json file the dictionary object by its id"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)

    return jsonify(obj.to_dict())


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def places_post(city_id):
    """Return json file the dictionary a newly added object"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)

    response = request.get_json()
    if response is None:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'user_id' not in response:
        return jsonify({'error': 'Missing user_id'}), 400
    elif storage.get(User, response['user_id']) is None:
        abort(404)
    elif 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400

    place = Place(**response, city_id=city_id)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    """Search"""
    response = request.get_json()
    if response is None:
        return jsonify({'error': 'Not a JSON'}), 400
    elif len(response) == 0 or all(len(v) == 0 for v in response.values()):
        return jsonify([obj.to_dict() for obj in storage.all(Place).values()])

    var = None
    if response.get('cities') and len(response.get('cities')) > 0:
        cities = response['cities']
        var = [v for v in storage.all(Place).values() if v.city_id in cities]
    if response.get('states') and len(response['states']) > 0:
        stats = response['states']
        if var:
            cities = [v.id for v in storage.all(
                City).values() if v.state_id in stats]
            var = [place
                   for place in storage.all(Place).values()
                   if place.city_id in cities and place.id
                   not in [v.id for v in var]] + var
        else:
            cities = [v.id for v in storage.all(
                City).values() if v.state_id in stats]
            var = [v for v in storage.all(
                Place).values() if v.city_id in cities]

    f = 0
    lis_places = []

    if response.get('amenities') and len(response.get('amenities')) > 0:
        f = 1
        if var:
            for v in var:
                lis = []
                for id in response['amenities']:
                    if id in [v.id for v in value.amenities]:
                        lis.append(True)
                    else:
                        lis.append(False)
            if all(lis):
                lis_places.append(value)
        else:
            for value in storage.all(Place).values():
                lis = []
                for id in response['amenities']:
                    if id in [v.id for v in value.amenities]:
                        lis.append(True)
                    else:
                        lis.append(False)
                if all(lis):
                    lis_places.append(value)
        places = [v.to_dict() for v in lis_places]
        for place in places:
            amenities = place['amenities']
            place['amenities'] = [am.to_dict() for am in amenities]
    if f:
        return jsonify(places)
    else:
        return jsonify([v.to_dict() for v in var])


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def places_delete(place_id):
    """Return json file an empty dictionary"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def places_put(place_id):
    """Return json file the dicionary object updated"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    response = request.get_json()
    if response is None:
        return jsonify({'error': 'Not a JSON'}), 400

    data = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']
    for k, v in response.items():
        if j not in data:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict()), 200
