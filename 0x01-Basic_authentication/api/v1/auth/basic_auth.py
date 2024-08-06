#!/usr/bin/env python3
"""
    BasicAuth .
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Basic auth class .
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        basic = "Basic "

        if not authorization_header or not isinstance(
                authorization_header, str):
            return None

        if not authorization_header.startswith(basic):
            return None

        return authorization_header[len(basic):]
