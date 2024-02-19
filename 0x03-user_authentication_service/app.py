#!/usr/bin/env python3
"""Flask app"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def message():
    """
    Returns a JSON response with a welcome message.

    :return: JSON response with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    email = request.form['email']
    password = request.form['password']
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
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


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Logs out the user by destroying the session associated with
    the user's session ID.

    Returns:
        - If the user is successfully logged out, redirects to the
        'message' page.
        - If the user is not logged in, aborts the request with a
        403 Forbidden error.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('message'))
    abort(403)


@app.route("/profile", strict_slashes=False)
def profile():
    """
    Retrieves the user's profile information.

    Returns:
        If the user is authenticated, returns a JSON
        response containing the user's email.
        If the user is not authenticated, returns a 403 Forbidden error.
    """
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email})
    abort(403)


@app.route("/reset_password", strict_slashes=False)
def reset_pwd():
    """
    Resets the password for a user.

    Retrieves the email from the request form, generates a reset
    password token using the AUTH module, and returns the email
    and reset token as a JSON response.

    Returns:
        A JSON response containing the email and reset token.

    Raises:
        403: If there is a ValueError while retrieving the email
        or generating the reset password token.
    """
    try:
        email = request.form['email']
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """
    Update the password for a user.

    :return: JSON response with email and success message if password
    update is successful.
    :rtype: flask.Response
    """
    email = request.form['email']
    reset_token = request.form['reset_token']
    new_pwd = request.form['new_password']

    try:
        AUTH.update_password(reset_token, new_pwd)
        return jsonify({"email": email, "message": 'Password updated'}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
