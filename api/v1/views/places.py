#!/usr/bin/python3
"""script that handles Place objects"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
@app_views.route("/cities/<city_id>/places/", methods=["GET"],
                 strict_slashes=False)
def places_by_city(city_id):
    """retrieves all Place objects by city
    Args:
        city_id: city id"""
    list_of_places = []
    if not storage.get("City", str(city_id)):
        abort(404)
    objs = storage.get("City", str(city_id))
    for obj in objs.places:
        list_of_places.append(obj.to_dict())
    return jsonify(list_of_places)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def place_create(city_id):
    """create place route
    Args:
        city_id: city id"""
    json_pls = request.get_json(silent=True)
    if json_pls is None:
        abort(400, 'Not a JSON')
    if not storage.get("City", str(city_id)):
        abort(404)
    if "user_id" not in json_pls:
        abort(400, 'Missing user_id')
    if not storage.get("User", json_pls["user_id"]):
        abort(404)
    if "name" not in json_pls:
        abort(400, 'Missing name')
    json_pls["city_id"] = city_id
    new_place = Place(**json_pls)
    new_place.save()
    response = jsonify(new_place.to_dict())
    response.status_code = 201
    return response


@app_views.route("/places/<place_id>",  methods=["GET"],
                 strict_slashes=False)
def place_by_id(place_id):
    """gets a specific Place object by ID
    Args:
        place_id: place object id"""
    if not storage.get("Place", str(place_id)):
        abort(404)
    objs = storage.get("Place", str(place_id))
    return jsonify(objs.to_dict())


@app_views.route("/places/<place_id>",  methods=["PUT"],
                 strict_slashes=False)
def place_put(place_id):
    """updates specific Place object by ID
    Args:
        place_id: Place object ID"""
    json_pls = request.get_json(silent=True)
    if json_pls is None:
        abort(400, 'Not a JSON')
    if not storage.get("Place", str(place_id)):
        abort(404)
    objs = storage.get("Place", str(place_id))
    for key, val in json_pls.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(objs, key, val)
    objs.save()
    return jsonify(objs.to_dict()), 200


@app_views.route("/places/<place_id>",  methods=["DELETE"],
                 strict_slashes=False)
def place_delete_by_id(place_id):
    """deletes Place by id
    Args:
        place_id: Place object id"""
    if not storage.get("Place", str(place_id)):
        abort(404)
    objs = storage.get("Place", str(place_id))
    storage.delete(objs)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places_search",  methods=["POST"],
                 strict_slashes=False)
def places_search():
    """search for places"""
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)
    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_of_places = []
        for place in places:
            list_of_places.append(place.to_dict())
        return jsonify(list_of_places)
    list_pls = []
    if states:
        st_objs = [stoeage.get(State, s_id) for s_id in states]
        for state in st_objs:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_pls.append(place)
    if cities:
        obj_cts = [storage.get(City, c_id) for c_id in cities]
        for ct in obj_cts:
            if ct:
                for place in ct.places:
                    if place not in list_pls:
                        list_pls.append(place)
    if amenities:
        if not list_pls:
            list_pls = storage.all(Place).values()
        objs_ams = [storage.get(Amenity, am_id) for am_id in amenities]
        list_pls = [place for place in list_pls
                    if all([am in place.amenities
                           for am in objs_ams])]
    places = []
    for pl in list_pls:
        dct = pl.to_dict()
        dct.pop('amenities', None)
        places.append(dct)
    return jsonify(places)
