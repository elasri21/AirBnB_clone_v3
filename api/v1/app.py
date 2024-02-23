#!/usr/bin/python3
"""Contains app, instance of Flask"""

from flask import Flask, jsonify
# from flask_cors import CORS
from os import getenv
from api.v1.views import app_views
from models import storage
app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """tear down storages"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", threaded=True)
