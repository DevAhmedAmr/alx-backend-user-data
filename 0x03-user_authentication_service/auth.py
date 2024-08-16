#!/usr/bin/env python3
"""
Authentication module
"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """
    function to hash a password

    Args:
        password (str): pw to be hashed

    Returns:
        bytes: hashed password
    """
    bytes = password.encode('utf-8')
    salt = gensalt()
    hash = hashpw(bytes, salt)
    return hash
