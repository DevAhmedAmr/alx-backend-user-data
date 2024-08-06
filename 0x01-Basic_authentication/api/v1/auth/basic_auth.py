#!/usr/bin/env python3
"""
    BasicAuth .
"""
# from api.v1.auth.auth import Auth
import base64
from auth import Auth


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


a = BasicAuth()

print(a.decode_base64_authorization_header(None))
print(a.decode_base64_authorization_header(89))
print(a.decode_base64_authorization_header("Holberton School"))
print(a.decode_base64_authorization_header("SG9sYmVydG9u"))
print(a.decode_base64_authorization_header("SG9sYmVydG9uIFNjaG9vbA=="))
print(a.decode_base64_authorization_header(
    a.extract_base64_authorization_header("Basic SG9sYmVydG9uIFNjaG9vbA==")))
