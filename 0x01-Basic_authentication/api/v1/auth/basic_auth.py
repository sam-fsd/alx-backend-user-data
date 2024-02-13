#!/usr/bin/env python3
"""Basic auth module"""
from api.v1.auth.auth import Auth
import base64


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
        if (base64_authorization_header is None or
                not isinstance(base64_authorization_header, str)):
            return None
        try:
            bytes_obj = base64_authorization_header.encode("utf-8")
            decoded = base64.b64decode(bytes_obj).decode("utf-8")
            return decoded
        except:
            return None
