#!/usr/bin/env python3
"""
    Session Auth .
"""
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User
import base64
from uuid import uuid4


class SessionAuth(Auth):
    """A class method to create a session auth class .
    """
    user_id_by_session_id: dict = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a new session id for user_id .

                Args:
                        user_id (str):. Defaults to None.

                Returns:
                        str: UUID
                """
        if not user_id or not isinstance(user_id, str):
            return None
        uuid = uuid4()
        self.user_id_by_session_id[uuid] = user_id

        return uuid
