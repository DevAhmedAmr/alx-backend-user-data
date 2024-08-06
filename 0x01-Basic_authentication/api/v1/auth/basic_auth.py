#!/usr/bin/env python3
"""
    BasicAuth .
"""
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User
import base64
# from auth import Auth


class BasicAuth(Auth):
    """
    Basic auth class .
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extract the base64 authorization header from the Authorization header .
        """
        basic = "Basic "

        if not authorization_header or not isinstance(
                authorization_header, str):
            return None

        if not authorization_header.startswith(basic):
            return None

        return authorization_header[len(basic):]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes a base64authorization header .

        Args:
            base64_authorization_header (str): base64 str

        Returns:
            str: decoded str
        """
        if not base64_authorization_header or not isinstance(
                base64_authorization_header, str):
            return None

        try:
            return base64.b64decode(
                base64_authorization_header
            ).decode("utf-8")

        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Extracts the user credentials from a given base64 encoded string .

        Args:
            decoded_base64_authorization_header ([str]):
                argument that credentials will be extracted from

        Returns:
            [tuple]: tuple of (username , password)
        """

        if not decoded_base64_authorization_header or not isinstance(
                decoded_base64_authorization_header, str) or \
                ":" not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(":"))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Returns a User object from credentials .

        Args:
            user_email ([str])
            user_pwd ([str])

        Returns:
            [User]: return user obj if correct credentials or None
        """
        if not user_email or not isinstance(user_email, str):
            return None

        if not user_pwd or not isinstance(user_pwd, str):
            return None
        users = User.search({"email": user_email})

        if not users:
            return None

        if not users[0].is_valid_password(user_pwd):
            return None

        return users[0]
