#!/usr/bin/env python3
""" session_auth views
"""
# POST / auth_session/login
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login',
                 methods=['POST'], strict_slashes=False)
def login() -> str:
    """ GET /api/v1/login
                login end point

    Return:
      - user object + session id in cookies
    """
    from api.v1.auth.session_auth import SessionAuth

    email = request.form.get("email")
    password = request.form.get("password")
    if not email:
        return {"error": "email missing"}, 400
    if not password:
        return {"error": "password missing"}, 400
    user = User.search({"email": email})
    if not user:
        return {"error": "no user found for this email"}, 404
    if not user[0].is_valid_password(password):
        return {"error": "wrong password"}, 401

    session_id = SessionAuth().create_session(user[0].id)

    respone = jsonify(user[0].to_json())
    respone.set_cookie(os.getenv("SESSION_NAME"), session_id)
    return respone
