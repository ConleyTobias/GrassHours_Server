from fastapi import FastAPI
from utils import *
import bcrypt
import datetime

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World!"}

@app.get("/login/{Username}/{Password}")
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


@app.get("/signup/{Username}/{Password}")
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
            "Denied": []
        }
        usernames_data[username] = next_user_id
        user_data["NextUserId"] += 1

        dump_json("Data/UserData.json", user_data)
        dump_json("Data/Usernames.json", usernames_data)

        return {"message": "Signup Successful"}

    except:
        return Exception("Something went wrong")

print(signup("new_2", "123456"))

@app.get("/changePassword/{Username}/{CurrentPassword}/{NewPassword}")
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

@app.get("/logData/{Username}/{Password}/{GrassHours}/{Description}")
def add_log(username: str, password: str, grass_hours: int, description: str):
    if login(username, password) == {"message": "Login Successful"}:
        queue = get_json("Data/Queue.json")
        next_id = str(queue["NextId"])
        queue[next_id] = {"Date": datetime.today(), "Username": username, "GrassHours": grass_hours, "Description": description}
        queue["NextId"] += 1

        dump_json("Data/Queue.json", queue)

@app.get("/getGrassHoursLeaderboard/top{number}")
def get_grass_hours_leaderboard(number: int):
    grass_hours_leaderboard = get_json("Data/GrassHoursLeaderboard.json")
    return grass_hours_leaderboard[:number]

@app.get("/getStreakLeaderboard/top{number}")
def get_streak_leaderboard(number: int):
    streak_leaderboard = get_json("Data/StreakLeaderboard.json")
    return streak_leaderboard[:number]

@app.get("/adminApprove/{id}/{EnteredAdminCode")
def admin_approve(id: int, entered_admin_code: str):
    admin_code = get_json("Data/AdminCode.json")
    queue = get_json("Data/Queue.json")
    user_data = get_json("Data/UserData.json")
    log_data = get_json("Data/LogData.json")
    usernames = get_json("Data/Usernames.json")

    if not bcrypt.checkpw(entered_admin_code.encode('utf-8'), admin_code["Code"].encode('utf-8')):
        return {"message": "Incorrect Password"}

    if id in queue:
        date = queue[id]["Date"]
        username = queue[id]["Username"]
        grass_hours = queue[id]["GrassHours"]
        user_id = str(usernames[username])

        if str(date)[:10] != user_data[user_id]["LastLogged"][:10]:
            user_data[user_id]["LastLogged"] = date
            user_data[user_id]["LastLogged"] = date

        user_data[user_id]["GrassHours"] += grass_hours

        log_data[username][id] = queue[id]
        del queue[id]

        dump_json("Data/Queue.json", queue)
        dump_json("Data/UserData.json", user_data)
        dump_json("Data/LogData.json", log_data)
        return {"message": "Approve Successful"}

    else:
        return {"message": "Id not found"}

@app.get("/adminDeny/{id}/{EnteredAdminCode}")
def admin_deny(id: int, entered_admin_code: str):
    user_data = get_json("Data/UserData.json")
    queue = get_json("Data/Queue.json")
    admin_code = get_json("Data/AdminCode.json")
    usernames = get_json("Data/Usernames.json")

    if not bcrypt.checkpw(entered_admin_code.encode('utf-8'), admin_code["Code"].encode('utf-8')):
        return {"message": "Incorrect Password"}

    username = queue[id]["Username"]
    user_id = str(usernames[username])
    user_data[user_id]["Denied"].append(id)
    return {"message": "Deny Successful"}

@app.get("/getQueue/{EnteredAdminCode}")
def get_queue(entered_admin_code: str):
    admin_code = get_json("Data/AdminCode.json")
    if not bcrypt.checkpw(entered_admin_code.encode('utf-8'), admin_code["Code"].encode('utf-8')):
        return {"message": "Incorrect Password"}

    return get_json("Data/Queue.json")

#TODO: test admin commands