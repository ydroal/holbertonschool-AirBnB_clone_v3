#!/usr/bin/python3
'''Module to set up rooting'''
from flask import jsonify
from . import app_views


@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})
