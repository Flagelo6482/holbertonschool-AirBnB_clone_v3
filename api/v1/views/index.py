#!/usr/bin/python3
"""New route"""
from flask import jsonify
from . import app_views
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """Return the status of our api"""
    dic = {"status": "OK"}
    return jsonify(dic)
