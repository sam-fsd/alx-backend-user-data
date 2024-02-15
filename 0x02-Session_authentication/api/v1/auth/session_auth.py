#!/usr/bin/env python3
"""Defines SessionAuth class that represents
   a custom session authenticator
"""

from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """
    This class represents the session-based authentication mechanism.
    It is responsible for managing user sessions and verifying session tokens.
    """
    pass
