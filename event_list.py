from flask import Blueprint, render_template, redirect, url_for, session
from datetime import datetime
from db_conn import db

event_list_bp = Blueprint('event_list', __name__)

@event_list_bp.route("/attend_event")#自己有報名的活動
def attend_event():
    if "username" in session:
        name = session["username"]
        collection = db["events"]
        collection1 = db['users']
        users = collection1.find(
            {"username": name}
        )
        for doc in users:
            level = doc['level']
        user_events = collection.find({"member": {"$in": [name]}})
        event_data = [{
        "_id": str(event["_id"]),
        "title": event["title"],
        "date_begin": event["date_begin"].split("T")[0], #取年月日
        "date_end": event["date_end"].split("T")[0],
        "organizing_group": event["tag"][0],
        "activity_type": event["tag"][1],
        "registration_status": "已報名",
        "remaining_quota": event["limit_value"] - len(event["member"])
        }
        for event in user_events]

        return render_template("home.html",
                               username = name, 
                               events = event_data,
                               level = level)
    else :
        return redirect(url_for('sign.index'))

@event_list_bp.route("/my_event")#自己創的活動
def my_event():
    if "username" in session:
        collection = db["events"]
        name = session["username"]
        result = collection.find({#找出主辦人有此user的活動
            "host" : name
        })
        event = []
        for doc in result:
            event.append(doc["title"])
        return render_template("home.html", username = name, title = event)
    else :
        return redirect("/error")
    
@event_list_bp.route("/end_event")#自己有參加(報名)且已結束的活動
def end_event():
    if "username" in session:
        # 獲取當前主機時間
        current_time = datetime.now()
        print(current_time)
        name = session["username"]
        collection = db["events"]
        collection1 = db['users']
        users = collection1.find(
            {"username": name}
        )
        for doc in users:
            level = doc['level']
        user_events = collection.find({
        "member": {"$in": [name]},
        })
        event_data = [{
        "_id": str(event["_id"]),
        "title": event["title"],
        "date_begin": event["date_begin"].split("T")[0], #取年月日
        "date_end": event["date_end"].split("T")[0],
        "organizing_group": event["tag"][0],
        "activity_type": event["tag"][1],
        "registration_status": "已報名",
        "remaining_quota": event["limit_value"] - len(event["member"])
        }
        for event in user_events if current_time > datetime.fromisoformat(event["date_end"])]

        return render_template("home.html",
                               username = name, 
                               events = event_data,
                               level = level)
    else :
        return redirect(url_for('sign.index'))