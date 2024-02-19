#!/usr/bin/env python3
"""The Auth module"""
import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hashes the given password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The hashed password.
    """
    password = password.encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The newly created user object.
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Checks if the login credentials provided are valid.

        Args:
            email (str): The email address of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the login credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            password = password.encode()
            if bcrypt.checkpw(password, user.hashed_password):
                return True
            return False
        except NoResultFound:
            return False

    def _generate_uuid(self) -> str:
        """returns a string repr of a new UUID"""
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """
        Creates a session for the user with the given email.

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID generated for the user.

        Raises:
            None
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            user.session_id = session_id
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Retrieves the user associated with the given session ID.

        Args:
            session_id (str): The session ID of the user.

        Returns:
            User: The user object associated with the session ID,
            or None if not found.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None
