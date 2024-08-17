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

    def create_session(self, email: str) -> str:
        """
        returns a new session Id

        Args:
            email (str): email

        Returns:
            [str]: a session string if user exists
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
        function to get user from_session id

        Args:
            session_id (str)

        Returns:
            User: user obj that is linked to session id
        """
        try:
            return self._db.find_user_by(session_id=session_id)

        except NoResultFound:
            return None

    def destroy_session(self, user_id: str):
        """
        function to delete or destroy session

        Args:
            user_id (str): user id to destroy it's session
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        - Find the user corresponding to the email.
        - If the user does not exist, raise a ValueError exception
        - If it exists, generate a UUID and update the user’s
            reset_token database field.

        Args:
            email (str)

        Returns:
            str: reset token
        """
        try:

            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token

        except NoResultFound:
            raise ValueError


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
