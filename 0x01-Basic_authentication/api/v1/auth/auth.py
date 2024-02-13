#!/usr/bin/env python3
"""
Defines Auth class for handling the API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    This class provides authentication functionality for the API.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required for a given path.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths that are
            excluded from authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """

        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        for p in excluded_paths:
            if p.rstrip("/") == path.rstrip("/"):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header for the given request.

        Args:
            request (Optional): The request object. Defaults to None.

        Returns:
            str: The authorization header.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current user based on the provided request.

        Args:
            request (Optional): The request object. Defaults to None.

        Returns:
            User: The current user object.
        """
        return None
