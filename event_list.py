from flask import Blueprint, render_template, redirect, session
from datetime import datetime
from db_conn import db

event_list_bp = Blueprint('event_list', __name__)

@event_list_bp.route("/attend_event")#自己有報名的活動
def attend_event():
    if "username" in session:
        collection = db["events"]
        name = session["username"]
        result = collection.find({#找出成員內有此user的活動
            "member" : name
        })
        event = []
        for doc in result:
            event.append(doc["title"])
        return render_template("home.html", username = name, title = event)
    else :
        return redirect("/error")

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
        collection = db["events"]
        name = session["username"]
        rightnow = datetime.now()#有import
        result = collection.find({#找出成員或主持內有此user且已過期的活動
            "$and" :[{
                {"date" : {"$lte" : rightnow}},
                {"$or" : [
                    {"member" : name},
                    {"host" : name}
                ]}
            }]
        })
        event = []
        for doc in result:
            event.append(doc["title"])
        return render_template("home.html", username = name, title = event)
    else :
        return redirect("/error")