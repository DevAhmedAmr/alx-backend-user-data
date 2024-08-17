#!/usr/bin/env python3
"""
Flask app
"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)

AUTH = Auth()


@app.route("/users", methods=["POST"])
def register():
    """ register a new user

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


@app.route("/")
def home():
    """ home dir

        Returns:
                message
        """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
