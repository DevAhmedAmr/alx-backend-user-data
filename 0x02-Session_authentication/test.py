#!/usr/bin/python3
""" Check response
"""
import requests
import base64

if __name__ == "__main__":
    user_email = "u5@hbtn.io"
    user_pwd = "pwd5"

    r = requests.post(
        'http://0.0.0.0:50000/api/v1/auth_session/login',
        data={
            'email': user_email,
            'password': user_pwd})
    if r.status_code != 200:
        print("Wrong status code: {}".format(r.status_code))
        exit(1)
    if r.headers.get('content-type') != "application/json":
        print("Wrong content type: {}".format(r.headers.get('content-type')))
        exit(1)

    try:
        r_json = r.json()

        r_user_email = r_json.get('email')
        if r_user_email is None:
            print("User is not return")
            exit(1)

        if r_user_email != user_email:
            print("User returned is not the same: {}".format(r_json))
            exit(1)

        print("OK", end="")
    except BaseException:
        print("Error, not a JSON")
