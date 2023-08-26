#!/usr/bin/python3
"""New route"""
from flask import jsonify
from . import app_views
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """Return the status of our api"""
    dictionary = {"status": "OK"}
    return jsonify(dictionary)
