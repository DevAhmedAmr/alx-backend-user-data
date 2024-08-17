#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth
from app import AUTH
email = 'bob@bob.com'
password = 'MyPwdOfBob'


print(AUTH.get_user_from_session_id("a2b2c57d-56e3-4da0-84de-557d97a3128c"))
print(AUTH._db.find_All_Users())
