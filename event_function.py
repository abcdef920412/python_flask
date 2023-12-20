from db_conn import db
from flask import session
from time import gmtime, strftime

def get_user_events(search_criteria):
    collection = db["events"]
    name = session["username"]
    user_events = collection.find(search_criteria)
    return [
        {
            "_id": str(event["_id"]),
            "title": event["title"],
            "host": event["host"],
            "date_begin": event["date_begin"], #取年月日
            "date_end": event["date_end"],
            "requirement": event["requirement"],
            "organizing_group": event["tag"][0],
            "activity_type": event["tag"][1],
            "registration_status": "已報名" if name in event["member"] else "未報名",
            "remaining_quota": event["limit_value"] - len(event["member"])
        }
        for event in user_events
    ]

def find_user_level(username):
    collection = db['users']
    user = collection.find_one(
        {"username": username}
    )
    return user["level"]

def find_user_identity(username):
    collection = db['users']
    user = collection.find_one(
        {"username": username}
    )
    return user["identity"]

def time_compare(data, mod):
    now = strftime("%Y-%m-%d  %H:%M", gmtime())
    new_data = []
    for x in data:
        if x["date_end"] > now and mod == 1:#attend_event(started + not start)
            new_data.append(x)
        if x["date_end"] < now and mod == 2:#end_event
            new_data.append(x)
    return new_data
