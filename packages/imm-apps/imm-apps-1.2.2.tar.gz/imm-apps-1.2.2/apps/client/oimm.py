import context
from datetime import date
import requests
import json
from source.excel import Excel
from pprint import pprint


def getJsonData(excel_file_name):
    e = Excel(excel_name=excel_file_name)
    return json.loads(e.json)


headers = {"accept": "application/json", "Content-Type": "application/json"}

# # make
# m5593 = {
#     "command": "make",
#     "model":"lmia-5593",
#     "output_name":"5593.xlsx",
# }

# fn=m5593['output_name']
# r = requests.post("http://localhost:8000/imm", json=m5593)

# with open(fn, 'wb') as f:
#     f.write(r.content)
# print(f"{fn} has been downloaded from web")

# # check
# m5593 = {
#     "command": "check",
#     "model":"lmia-5593",
#     "data":getJsonData("/Users/jacky/desktop/demo/5593.xlsx"),
#     # "output_name":"5593.xlsx",
# }
# r = requests.post("http://localhost:8000/imm", json=m5593)
# if r.status_code==200:
#     print(r.json()["success"])
# elif r.status_code==422:
#     print(r.json()['detail'])

# # word
# m5593={
#     "command": "word",
#     "model": "lmia-5593",
#     "data":getJsonData("/Users/jacky/desktop/demo/5593.xlsx"),
#     "output_name": "sl.docx",
#     "print_json": True,
#     "doctype": "sl",
#     "rciccompany": "noah",
#     "tempnum": 1,
# }
# r = requests.post("http://localhost:8000/imm", json=m5593)
# fn=m5593['output_name']
# with open(fn, 'wb') as f:
#     f.write(r.content)
# print(f"{fn} has been downloaded from web")


# #webform
# m5593={
#     "command": "webform",
#     "model": "lmia-5593",
#     "data":getJsonData("/Users/jacky/desktop/demo/5593.xlsx"),
#     "output_name": "5593.json",
#     "rcic": "jacky",
#     "upload_dir":"."
# }
# r = requests.post("http://localhost:8000/imm", json=m5593)
# fn=m5593['output_name']
# with open(fn, 'wb') as f:
#     f.write(r.content)
# print(f"{fn} has been downloaded from web")

# # pdfform
# m5709 = {
#     "command": "pdfform",
#     "model": "5709",
#     "data": getJsonData("/Users/jacky/desktop/demo/5709.xlsx"),
#     "output_name": "5709.json",
#     "rcic": "jacky",
#     "upload_dir": ".",
# }
# r = requests.post("http://localhost:8000/imm", json=m5709)
# fn = m5709["output_name"]
# with open(fn, "wb") as f:
#     f.write(r.content)
# print(f"{fn} has been downloaded from web")

# cap={
#     "command": "run",
#     "model": "lmia-cap",
#     "data":getJsonData("/Users/jacky/desktop/demo/cap.xlsx"),
# }
# r = requests.post("http://localhost:8000/imm", json=cap)

# if r.status_code==200:
#     print(r.json()["success"])
# elif r.status_code==422:
#     print(r.json()['detail'])


# get user
r = requests.get("http://localhost:8000/user")
pprint(r.json())

# # read
# r = requests.get("http://localhost:8000/user/630aa43fb5e1ee46a63716f6")
# print(r.status_code, r.content)

# create user
# jacky = {
#     "username": "may",
#     "email": "jackyzhang1969@gmail.com",
#     "phone": "7783215110",
#     "password": "555",
# }
# r = requests.post("http://localhost:8000/user/", json=jacky)
# print(r.status_code, r.content)

# update
# jacky = {
#     "username": "lele",
#     "email": "jackyzhang1969@gmail.com",
#     "phone": "7783215110",
#     "password": "xxxxx",
# }
# r = requests.put("http://localhost:8000/user/630aa056f0e34b68a8d7b9bf", json=jacky)
# print(r.status_code, r.content)

# # delete
# r = requests.delete("http://localhost:8000/user/630aa056f0e34b68a8d7b9bf")
# print(r.status_code, r.content)
