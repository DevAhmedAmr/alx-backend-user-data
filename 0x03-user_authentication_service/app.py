#!/usr/bin/env python3
"""
Flask app
"""
from flask import Flask, jsonify
from auth import Auth

app = Flask(__name__)

AUTH = Auth()


@app.route("/", method=["POST"])
def login():
    """ home dir

        Returns:
                message
        """
    return jsonify({"message": "Bienvenue"})


@app.route("/")
def home():
    """ home dir

        Returns:
                message
        """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
