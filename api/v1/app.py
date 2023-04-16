#!/usr/bin/python3
'''Module to return the status of API'''
from flask import jsonify
from flask import Flask
import os
from api.v1.views import app_views
from models import storage
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.errorhandler(404)
def error_404(error):
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def close_storage(exception=None):
    storage.close()


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
