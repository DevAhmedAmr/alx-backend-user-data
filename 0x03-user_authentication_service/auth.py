#!/usr/bin/env python3
"""Authentication module."""

from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Class to interact with the authentication database."""

    def __init__(self):
        """Initialize the Auth class with a database instance."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user.

        Args:
            email (str): User's email.
            password (str): User's password.

        Raises:
            ValueError: If the user already exists.

        Returns:
            User: The newly created User object.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(
                email=email, hashed_password=_hash_password(password))
        raise ValueError(f"User {email} already exists.")

    def valid_login(self, email: str, password: str) -> bool:
        """
        Verify credentials for email and password.

        Args:
            email (str): User's email.
            password (str): User's password.

        Returns:
            bool: True if the credentials are correct, otherwise False.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return checkpw(password.encode("utf-8"), user.hashed_password)

    def create_session(self, email: str) -> str:
        """
        Create a new session ID.

        Args:
            email (str): User's email.

        Returns:
            str: The session string if the user exists, otherwise None.
        """
        try:
            user = self._db.find_user_by(email=email)
            uuid = _generate_uuid()
            self._db.update_user(user_id=user.id, session_id=uuid)
            return uuid
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Retrieve a user based on the session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            User: The User object linked to the session ID, or None if not found.
        """
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str):
        """
        Destroy the session for the given user ID.

        Args:
            user_id (str): The user's ID.
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a reset password token.

        Args:
            email (str): The user's email.

        Returns:
            str: The reset token.

        Raises:
            ValueError: If the user does not exist.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str):
        """
        Update the user's password.

        Args:
            reset_token (str): The reset token.
            password (str): The new password.

        Raises:
            ValueError: If the reset token is invalid.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        self._db.update_user(
            user.id,
            hashed_password=_hash_password(password),
            reset_token=None
        )


def _hash_password(password: str) -> bytes:
    """
    Hash a password.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The hashed password.
    """
    bytes_password = password.encode('utf-8')
    salt = gensalt()
    hashed = hashpw(bytes_password, salt)
    return hashed


def _generate_uuid() -> str:
    """
    Generate a UUID.

    Returns:
        str: The generated UUID.
    """
    from uuid import uuid4
    return str(uuid4())
