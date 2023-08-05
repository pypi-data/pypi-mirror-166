import requests
from pprint import pprint


def login(email, password):
    session = requests.Session()
    payload = {"username": email, "password": password}
    res = session.post("http://127.0.0.1:8000/login", data=payload)
    session.headers.update(
        {
            # "Content-Type": "application/x-www-form-urlencoded",
            "Content-Type": "application/json",
            "Authorization": f"{res.json()['token_type']} {res.json()['access_token']}",
        }
    )
    return session


def get_session():
    # email = input("Input your email: ")
    # psw = getpass()
    email = "jacky@gmail.com"
    psw = "111"
    return login(email, psw)
