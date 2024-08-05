#!/usr/bin/env python3
"""
Encrypting passwords
"""

import bcrypt

# example password


def hash_password(password: str) -> bytes:
    """Hash a password

    Args:
        password ([type]): [description]

    Returns:
        str: hashed password
    """
    # converting password to array of bytes
    bytes = password.encode('utf-8')

    # generating the salt
    salt = bcrypt.gensalt()

    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)
    return hash


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if the given password is valid for the given password .
    """
    pw = password.encode('utf-8')
    result = bcrypt.checkpw(pw, hashed_password)
    return result
