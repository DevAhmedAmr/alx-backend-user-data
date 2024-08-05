#!/usr/bin/env python3
"""
Encrypting passwords
"""

import bcrypt

# example password


def hash_password(password):
    # converting password to array of bytes
    bytes = password.encode('utf-8')

    # generating the salt
    salt = bcrypt.gensalt()

    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)
    return hash
