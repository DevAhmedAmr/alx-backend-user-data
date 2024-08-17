#!/usr/bin/env python3
"""
Authentication module
"""
from bcrypt import hashpw, gensalt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from bcrypt import checkpw


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        register a new user

        Args:
            email (str)
            password (str)

        Raises:
            ValueError : if user already exist

        Returns:
            newly created User obj
        """
        try:
            self._db.find_user_by(email=email)

        except NoResultFound:

            return self._db.add_user(
                email=email,
                hashed_password=_hash_password(password))

        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        verify Credentials for email and password

        Args:
            email (str)
            password (str)

        Returns:
            bool: True if email and password are correct otherwise
                  False
        """
        try:

            user = self._db.find_user_by(email=email)

        except NoResultFound:
            return False

        return checkpw(password.encode("utf-8"), user.hashed_password)


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


def _generate_uuid() -> str:
    """
    generate uuid

    Returns:
        str: uuid
    """
    from uuid import uuid4
    return str(uuid4())
