#!/usr/bin/python3
"""new view forCity objects that handles all default RESTFul API actions"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def city_by_state(state_id):
    """Retrieves the list of all City objects"""
    list_of_cities = []
    objects = storage.get("State", state_id)
    if objects is None:
        abort(404)
    for obj in objects.cities():
        list_of_cities.append(obj.to_dict())
    return jsonify(list_of_cities)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def city_create(state_id):
    """Creates a City: POST /api/v1/cities
    Args:
        state_id: state id"""
    json_cts = request.get_json(silent=True)
    if json_cts is None:
        abort(400, 'Not a JSON')
    if not storage.get("State", str(state_id)):
        abort(404)
    if "name" not in json_cts:
        abort(400, 'Missing name')
    json_cts["state_id"] = state_id
    new_c = City(**json_cts)
    new_c.save()
    response = jsonify(new_c.to_dict())
    response.status_code = 201
    return response


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
        if k not in ["id", "create_at", "update_at"]:
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
