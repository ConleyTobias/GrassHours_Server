from fastapi import FastAPI
from utils import *
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World!"}


@app.get("/login/{Username}")
def login(username: str, password: str):
    path = "Data/UserData.json"
    with open(path, 'r') as file:
        data = json.load(file)
    #if :


@app.get("/signup/{Username}")
def signup(username: str, password: str):
    with open("Data/UserData.json", 'r') as user_data_file:
        user_data = json.load(user_data_file)

    with open("Data/Usernames.json", 'r') as username_file:
        usernames_data = json.load(username_file)

    if username in usernames_data:
        return Exception("Username already exists")

    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    except:
        return Exception("Password didn't hash correctly")

    try:
        next_user_id = user_data["NextUserId"]
        str_next_user_id = str(next_user_id)
        user_data[str_next_user_id] = {
            "UserId": next_user_id,
            "Username": username,
            "Password": hashed_password.decode('utf-8'),
            "GrassHours": 0,
            "Streak": 0,
            "LastLogged": "",
        }
        usernames_data[username] = next_user_id
        user_data["NextUserId"] += 1

        print(user_data)
        with open('Data/UserData.json', 'w') as user_data_file:
            json.dump(user_data, user_data_file, indent=4)  # Use indent for pretty formatting

        print(usernames_data)
        with open('Data/Usernames.json', 'w') as username_file:
            json.dump(usernames_data, username_file, indent=4)  # Use indent for pretty formatting

        return "success"

    except:
        return Exception("Something went wrong")


print(signup("new_John Doe", "123456"))
