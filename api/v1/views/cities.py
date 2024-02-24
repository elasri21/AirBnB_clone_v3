#!/usr/bin/python3
"""new view forCity objects that handles all default RESTFul API actions"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
@app_views.route("/states/<state_id>/cities/", methods=["GET"],
                 strict_slashes=False)
def city_by_state(state_id):
    """Retrieves the list of all City objects"""
    list_of_cities = []
    objects = storage.get("State", state_id)
    if objects is None:
        abort(404)
    for obj in objects.cities:
        list_of_cities.append(obj.to_dict())
    return jsonify(list_of_cities)

@app_views.route('/states/<state_id>/cities', methods=['POST'])
@app_views.route('/states/<state_id>/cities/', methods=['POST'])
def create_city(state_id):
    '''Creates a City'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    all_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if state_obj == []:
        abort(404)
    cities = []
    new_city = City(name=request.json['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()
    cities.append(new_city.to_dict())
    return jsonify(cities[0]), 201


@app_views.route("/citiess/<city_id>",  methods=["GET"], strict_slashes=False)
def city_by_id(city_id):
    """get a city with aspecific id
    Args:
        city_id: city id"""
    obj = storage.get("City", str(city_id))
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route("/cities/<city_id>",  methods=["PUT"], strict_slashes=False)
def city_put(city_id):
    """update a city with the id passed
    Args:
        city_id: city id"""
    cts_json = request.get_json(silent=True)
    if cts_json is None:
        abort(400, "Not a JSON")
    obj = storage.get("City", str(city_id))
    if obj is None:
        abort(404)
    for k, v in cts_json.items():
        if k not in ["id", "create_at", "update_at", "state_id"]:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def city_delete_by_id(city_id):
    """Delete a city with a specific if
    Args:
        city_id: city id"""
    obj = storage.get("City", str(city_id))
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({})
