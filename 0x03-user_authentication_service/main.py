#!/usr/bin/env python3
"""
Main file
"""
from sqlalchemy import select
from db import User
from auth import Auth
from db import DB
db = DB()
db.find_All_Users()

email = 'me@me2.com'
password = 'mySecuredPwd'

auth = Auth()

try:
    user = auth.register_user(email, password)
    user = auth.register_user(email + "2", password)
    print("successfully created a new user!")
except ValueError as err:
    print("could not create a new user: {}".format(err))

try:
    user = auth.register_user(email, password)
    print("successfully created a new user!")
except ValueError as err:
    print("could not create a new user: {}".format(err))
############################################################
users = db.find_All_Users()
