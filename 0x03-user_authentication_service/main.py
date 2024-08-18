#!/usr/bin/env python3
"""Main file."""
from auth import Auth
from app import AUTH
email = 'bob@bob.com'
password = 'MyPwdOfBob'

user = AUTH._db.find_user_by(email=email)
print(user.hashed_password)
reset_token = AUTH.get_reset_password_token(email)
print("toeken= ", AUTH._db.find_user_by(email=email).reset_token)

AUTH.update_password(reset_token, "new_password")
print(AUTH._db.find_user_by(email=email).hashed_password)
print(AUTH._db.find_user_by(email=email).reset_token)
