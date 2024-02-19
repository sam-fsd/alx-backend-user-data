#!/usr/bin/env python3
"""Flask app"""
from flask import Flask, jsonify, request, abort
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route("/")
def message():
    """
    Returns a JSON response with a welcome message.

    :return: JSON response with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users():
    email = request.form['email']
    password = request.form['password']
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'])
def login():
    """
    Logs in a user by validating their email and password.

    Returns:
        A JSON response containing the user's email and a success message.

    Raises:
        HTTPException: If the login credentials are invalid (status code 401).
    """
    email = request.form['email']
    password = request.form['password']

    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    res = jsonify({"email": email, "message": "logged in"})
    res.set_cookie("session_id", session_id)
    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
