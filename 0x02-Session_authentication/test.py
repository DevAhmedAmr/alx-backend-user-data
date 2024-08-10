#!/usr/bin/python3
""" Check response
"""
import requests
import base64
# curl "http://0.0.0.0:5000/api/v1/auth_session/login" -XPOST -d
# "email=bobsession@hbtn.io" -d "password=fake pwd" -vvv

r = requests.post(
    "http://0.0.0.0:50000/api/v1/auth_session/login",
    data={"email": "bobsession@hbtn.io", "password": "fake pwd"})
session_id = r.cookies.get("_my_session_id")

r = requests.get(
    "http://0.0.0.0:50000/api/v1/users/me",
    cookies={"_my_session_id": session_id})

r = requests.delete("http://0.0.0.0:50000/api/v1/auth_session/logout",

                    cookies={"_my_session_id": session_id})
print(r.content)
