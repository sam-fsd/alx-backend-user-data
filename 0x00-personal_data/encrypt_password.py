#!/usr/bin/env python3
"""defines a function that hashes a password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password, which is a byte string"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """returns a boolean"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
