#!/usr/bin/env python3
"""The Auth module"""
import bcrypt


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
