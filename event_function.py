from db_conn import db
from flask import session

def get_user_events(search_criteria):
    collection = db["events"]
    name = session["username"]
    user_events = collection.find(search_criteria)
    return [
        {
            "_id": str(event["_id"]),
            "title": event["title"],
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