#!/usr/bin/env python3
"""
Flask app
"""
from flask import Flask, jsonify, request, abort, make_response
from auth import Auth
from flask import Response
app = Flask(__name__)

AUTH = Auth()


@app.route("/sessions", methods=["DELETE"])
def logout():
    """
    logout : deletes -> destroys session id
    """
    session_id = request.cookies.get('session_id')

    if not session_id:
        return Response(status=404)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        return Response(status=403)

    AUTH.destroy_session(user.id)
    return Response(status=302)


@app.route("/users", methods=["POST"])
def register():
    """
    register a new user

        Returns:
                status 200 if created successfully or
                400 if user already exist
        """
    email = request.form.get("email")
    password = request.form.get("password")

    if email and password:

        try:
            AUTH.register_user(email, password)

            return jsonify(
                {"email": email, "message": "user created"}
            )
        except ValueError:
            return jsonify(
                {"message": "email already registered"}
            ), 400


@app.route("/sessions", methods=["POST"])
def login():
    """
        endpoint to login and returns session id as a response cookie

    Returns:
        [response]: response confirming succeeded in logging in  or not
        session id as a response cookie
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)

    session = AUTH.create_session(email)

    res = make_response(jsonify({"email": email, "message": "logged in"}))

    res.set_cookie("session_id", session)

    return res


@app.route("/")
def home():
    """ home dir

        Returns:
                message
        """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
