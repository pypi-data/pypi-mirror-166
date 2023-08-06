import context
from datetime import date
import httpx
import json
from source.excel import Excel
from pprint import pprint


def getJsonData(excel_file_name):
    e = Excel(excel_name=excel_file_name)
    return json.loads(e.json)


# get user
def login(email, password):
    client = httpx.Client()
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    r = client.post(
        "http://localhost:8000/login/",
        json={"username": email, "password": password},
        # headers=headers,
    )
    print(r.content)
    token = json.loads(r.content)["access_token"]
    client.headers.update({"authorization": token})
    print(r.content)
    return client


client = login("jackyson@gmail7.com", "777")
r = client.get("http://localhost:8000//user")
print(r)

# # read
# r = httpx.get("http://localhost:8000/user/630aa43fb5e1ee46a63716f6")
# print(r.status_code, r.content)

# # create user
# jacky = {
#     "username": "may",
#     "email": "jacky2@gmail.com",
#     "phone": "7783215110",
#     "password": "222",
# }
# r = httpx.post("http://localhost:8000/user/", json=jacky)
# print(r.status_code, r.content)

# update
# jacky = {
#     "username": "lele",
#     "email": "jackyzhang1969@gmail.com",
#     "phone": "7783215110",
#     "password": "xxxxx",
# }
# r = httpx.put("http://localhost:8000/user/630aa056f0e34b68a8d7b9bf", json=jacky)
# print(r.status_code, r.content)

# # delete
# r = httpx.delete("http://localhost:8000/user/630aa056f0e34b68a8d7b9bf")
# print(r.status_code, r.content)
