#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth
from app import AUTH
email = 'bob@bob.com'
password = 'MyPwdOfBob'

USER = AUTH.get_user_from_session_id("741c6e65-ed07-40db-be26-2c31ff6eaa41")
print("SESSION= ", USER.session_id)
