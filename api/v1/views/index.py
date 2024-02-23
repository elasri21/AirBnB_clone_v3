#!/usr/bin/python3
"""Contains routes of the app"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """status route
    Return: JSON representation of the response"""
    data = {
            "status": "OK"
           }
    response = jsonify(data)
    response.status_code = 200
    return response
