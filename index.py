from fastapi import FastAPI
from utils import *
import bcrypt

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World!"}


@app.get("/login/{Username}")
def login(username: str, entered_password: str):
    user_data = get_json("Data/UserData.json")
    username_data = get_json("Data/Usernames.json")

    if username not in user_data:
        return {"message": "Username not found"}

    user_id = str(username_data[username])
    current_password = user_data[user_id]['Password'].encode('utf-8')
    if bcrypt.checkpw(entered_password.encode('utf-8'), current_password):
        return {"message": "Login Successful"}
    else:
        return {"message": "Incorrect Password"}


@app.get("/signup/{Username}")
def signup(username: str, password: str):
    user_data = get_json("Data/UserData.json")
    usernames_data = get_json("Data/Usernames.json")

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

        dump_json("Data/UserData.json", user_data)
        dump_json("Data/Usernames.json", usernames_data)

        return {"message": "Signup Successful"}

    except:
        return Exception("Something went wrong")

print(signup("new_2", "123456"))

@app.get("/changePassword/{Username}")
def change_password(username: str, current_password: str, new_password: str):
    user_data = get_json("Data/UserData.json")
    usernames_data = get_json("Data/Usernames.json")

    if login(username, current_password) == {"message": "Login Successful"}:
        try:
            user_id = str(usernames_data[username])
            user_data[user_id]['Password'] = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        except:
            return Exception("Something went wrong")
        return {"message": "Change Password Successful"}
    else:
        return login(username, current_password)