#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth
from app import AUTH
email = 'bob@bob.com'
password = 'MyPwdOfBob'

USER = AUTH.get_user_from_session_id("70b5bab6-852b-4923-af0c-093c66011f3d")
print(USER)
print(AUTH._db.find_All_Users())
AUTH.destroy_session(USER.id)
print("SESSION= ", USER.session_id)
