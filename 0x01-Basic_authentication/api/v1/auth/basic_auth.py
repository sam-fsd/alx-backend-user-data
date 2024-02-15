#!/usr/bin/env python3
"""Basic auth module"""
from api.v1.auth.auth import Auth
import base64
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    BasicAuth class represents the basic authentication mechanism.
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the base64 encoded authorization header value.

        Args:
            authorization_header (str): The authorization header string.

        Returns:
            str: The base64 encoded value extracted from the
            authorization header.
        """
        if (authorization_header is None or
            not isinstance(authorization_header, str)
                or "Basic " not in authorization_header):

            return None
        val = authorization_header.split(' ')[1]
        return val

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decode a base64 encoded authorization header.

        Args:
            base64_authorization_header (str): The base64 encoded
            authorization header.

        Returns:
            str: The decoded authorization header.

        """
        if (base64_authorization_header is None or
                not isinstance(base64_authorization_header, str)):
            return None
        try:
            bytes_obj = base64_authorization_header.encode("utf-8")
            decoded = base64.b64decode(bytes_obj).decode("utf-8")
            return decoded
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        Extracts the user credentials from the decoded base64
        authorization header.

        Args:
            decoded_base64_authorization_header (str): The decoded base64
            authorization header.

        Returns:
            Tuple[str, str]: A tuple containing the user and email extracted
            from the header.
        """
        if (decoded_base64_authorization_header is None or
                not isinstance(decoded_base64_authorization_header, str)
                or ":" not in decoded_base64_authorization_header):
            return (None, None)
        user, email = decoded_base64_authorization_header.split(':')
        return (user, email)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Retrieve a user object based on the provided credentials.

        Args:
            user_email (str): The email of the user.
            user_pwd (str): The password of the user.

        Returns:
            User: The user object if the credentials are valid, otherwise None.
        """
        if (user_email is None or not isinstance(user_email, str) or
                user_pwd is None or not isinstance(user_pwd, str)):
            return None
        try:
            user = User.search({"email": user_email})
            if user is None or not user.is_valid_password(user_pwd):
                return None
            return user
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current user based on the provided request.

        Args:
            request (Optional): The request object. Defaults to None.

        Returns:
            User: The current user object.
        """
        try:
            auth_header = self.authorization_header(request)
            encoded_header = self.extract_base64_authorization_header(
                auth_header)
            decoded_header = self.decode_base64_authorization_header(
                encoded_header)
            user, pwd = self.extract_user_credentials(decoded_header)
            return self.user_object_from_credentials(user, pwd)
        except Exception:
            return None
