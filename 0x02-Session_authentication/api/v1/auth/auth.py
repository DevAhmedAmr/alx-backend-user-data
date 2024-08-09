#!/usr/bin/env python3
""" Auth class. """
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """A class method that handles the Auth class .
        """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require authentication to be used for this client .

                Args:
                        path (str): [description]
                        excluded_paths (List[str]): [description]

                Returns:
                        bool: [description]
                """
        if (not path) or not excluded_paths:
            return True

        if (path in excluded_paths or (path + "/") in excluded_paths):
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """ the Authorization header for the request .

                Args:
                        request ([type], optional): [description].
                        Defaults to None.

                Returns:
                        str: Authorization header
                """
        if not request or not request.headers.get("Authorization"):
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """Return the current user s current user .

                Returns:
                        [type]: [description]
                """
        return None

    def session_cookie(self, request=None):
        """Returns the session cookie if it is not set .

            Args:
                request ([flask_request], optional): Defaults to None.

            Returns:
                [dict]: cookie value from request
            """
        if request is None:
            return request

        return request.cookies.get(os.getenv("SESSION_NAME"))
# SESSION_NAME
