#!/usr/bin/env python3
"""Flask app"""
from flask import Flask, jsonify, request, abort, make_response
from auth import Auth
from flask import Response
app = Flask(__name__)

AUTH = Auth()


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """PUT End point to reset password
    it requires: email , token and new password

    Returns:
        Response: 200 if success .
                403 if user does not exist"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        return abort(403)

    return make_response(
        jsonify({"email": email, "message": "Password updated"})
    )


@app.route("/reset_password", methods=["POST"])
def reset_password():
    """Post End point to get reset_password token
    it requires: email

    Returns:
        Response:

        reset_password token and  200 if success .
        403 if user does not exist"""
    email = request.form.get("email")

    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        return abort(403)

    return make_response(
        jsonify({"email": email, "reset_token": token})
    )


@app.route("/profile", methods=["GET"])
def profile():
    """GET End point to get user profile via session_id
    it requires: session_id

    Returns:
        Response:
        dictionary of user profile and 200 .
            or    403 if session id is invalid"""

    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if not user or not session_id:
        return abort(403)

    res = make_response(jsonify({"email": user.email}))
    res.status_code = 200
    return res


@app.route("/sessions", methods=["DELETE"])
def logout():
    """logout : deletes -> destroys session id"""
    session_id = request.cookies.get('session_id')

    if not session_id:
        return Response(status=403)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        return Response(status=403)

    AUTH.destroy_session(user.id)
    return Response(status=302)


@app.route("/users", methods=["POST"])
def register():
    """register a new user

        Returns:
                status 200 if created successfully or
                400 if user already exist"""
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
    """endpoint to login and returns session id as a response cookie

    Returns:
        [response]: response confirming succeeded in logging in  or not
        session id as a response cookie"""

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
    """home dir

        Returns:
                message"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
