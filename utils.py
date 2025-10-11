from datetime import datetime
import time
import json

def log(func):
    def wrapper():
        start = time.perf_counter()
        func()
        print(f"{func.__name__}() ran @{datetime.now()}, taking {time.perf_counter() - start} seconds)")
    return wrapper

def get_json(path):
    with open(path, 'r') as file:
        return json.load(file)

def dump_json(path, data):
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

def add_to_leaderboards(user_id, username, grass_hours, streak):
    grass_hours_leaderboard = get_json("GrassHoursLeaderboard.json")
    streak_leaderboard = get_json("StreakLeaderboard.json")

    for i in range(grass_hours_leaderboard):
        if grass_hours_leaderboard[i]["grass_hours"] > grass_hours:
            pass
        elif grass_hours_leaderboard[i]["grass_hours"] == grass_hours:
            grass_hours_leaderboard.insert(i-1, {"user_id": user_id, "username": username, "grass_hours": grass_hours})
            break
        else:
            grass_hours_leaderboard.insert(i, {"user_id": user_id, "username": username, "grass_hours": grass_hours})
            break

    for i in range(streak_leaderboard):
        if streak_leaderboard[i]["streak"] > streak:
            pass
        elif streak_leaderboard[i]["streak"] == streak:
            streak_leaderboard.insert(i - 1, {"user_id": user_id, "username": username, "streak": streak})
            break
        else:
            streak_leaderboard.insert(i, {"user_id": user_id, "username": username, "streak": streak})
            break

        dump_json("StreakLeaderboard.json", streak_leaderboard)
        dump_json("StreakLeaderboard.json", streak_leaderboard)