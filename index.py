from fastapi import FastAPI
from utils import *
import json

app = FastAPI()

"""
Json read & write
    path = "SOMETHING"

    with open(path, 'r') as file:
        data = json.load(file)

    with open(path, 'w') as file:
        json.dump(data, file, indent=4)  # Use indent for pretty formatting
"""

@app.get("/")
def read_root():
    return {"message": "Hello World!"}

@app.get("/login/{Username}")
def login(username: str, password: str):
    path = "Data/UserData.json"
    with open(path, 'r') as file:
        data = json.load(file)
    #if data["password"] != password:

@app.get("/signup/{Username}")
def signup(username: str, password: str):
    path = "Data/UserData.json"
    with open(path, 'r') as file:
        data = json.load(file)

    data["UserId"].append(data["LastUserId"])
    data["LastUserId"] += 1
    data["Username"].append(username)
    data["Password"].append(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))
    data["GrassHours"].append(0)
    data["Streak"].append(0)
    data["LastLogged"].append("")