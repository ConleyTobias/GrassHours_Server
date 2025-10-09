from math import nextafter

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
    with open("Data/UserData.json", 'r') as file:
        UserData = json.load(file)

    with open("Data/Usernames.json", 'r') as file:
        Usernames = json.load(file)
        
    next_user_id = UserData["NextUserId"]
    str_next_user_id = str(next_user_id)
    UserData[str_next_user_id] = {}
    UserData[str_next_user_id]["UserId"] = next_user_id
    UserData[str_next_user_id]["Username"] = username
    UserData[str_next_user_id]["Password"] = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    UserData[str_next_user_id]["GrassHours"] = 0
    UserData[str_next_user_id]["Streak"] = 0
    UserData[str_next_user_id]["LastLogged"] = ""
    Usernames[username] = next_user_id
    UserData["NextUserId"] += 1

signup("John Doe", "123456")