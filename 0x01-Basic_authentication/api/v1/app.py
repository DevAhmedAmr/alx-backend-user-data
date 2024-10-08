#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
auth = os.getenv("AUTH_TYPE")

if auth:
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def Unauthorized_err(error) -> str:
    """
    Not found handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_err(error) -> str:
    """
    Not found handler
    """
    return jsonify({"error": "Forbidden"}), 403


def before_request():
    """
    Checks if the user has authorized to access the request .
    """

    if not auth:
        return
    if not auth.require_auth(request.path, [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/']
    ):
        return
    if not auth.authorization_header(request):
        abort(401)
    if not auth.current_user(request):
        abort(403)


app.before_request(before_request)

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
