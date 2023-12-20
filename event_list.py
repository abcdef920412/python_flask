from flask import Blueprint, render_template, redirect, url_for, session
from datetime import datetime
from db_conn import db
from event_function import get_user_events, find_user_level, find_user_identity

event_list_bp = Blueprint('event_list', __name__)

@event_list_bp.route("/joinable_event")#未報名且符合資格，尚可報名的活動
def joinable_event():
    if "username" in session:
        # 獲取當前主機時間
        current_time = datetime.now()
        name = session["username"]
        level = find_user_level(name)
        identity = find_user_identity(name)
        search_criteria = { #未報名且符合資格
        "$and": [
            {"member": {"$nin": [name]}},
            {"requirement": {"$in": [identity, "all"]}}
        ]}
        event_data = [
            event
            for event in get_user_events(search_criteria)
            if current_time <= datetime.fromisoformat(event["date_end"])
        ]

        return render_template("home.html",
                               username = name, 
                               events = event_data,
                               level = level)
    else :
        return redirect(url_for('sign.index'))

@event_list_bp.route("/end_event")#所有已經結束的活動
def end_event():
    if "username" in session:
        # 獲取當前主機時間
        current_time = datetime.now()
        name = session["username"]
        level = find_user_level(name)
        
        event_data = [
            event
            for event in get_user_events({})
            if current_time > datetime.fromisoformat(event["date_end"])
        ]

        return render_template("home.html",
                               username = name, 
                               events = event_data,
                               level = level)
    else :
        return redirect(url_for('sign.index'))    

@event_list_bp.route("/attend_event")#自己有報名的活動，且活動未結束
def attend_event():
    if "username" in session:
        # 獲取當前主機時間
        current_time = datetime.now()
        name = session["username"]
        level = find_user_level(name)
        search_criteria = {
            "member": {"$in": [name]}
        }
        event_data = [
            event
            for event in get_user_events(search_criteria)
            if current_time <= datetime.fromisoformat(event["date_end"])
        ]
        
        return render_template("home.html",
                               username = name, 
                               events = event_data,
                               level = level)
    else :
        return redirect(url_for('sign.index'))
    
@event_list_bp.route("/user_ended_event")#自己有參加(報名)且已結束的活動
def user_ended_event():
    if "username" in session:
        # 獲取當前主機時間
        current_time = datetime.now()
        name = session["username"]
        level = find_user_level(name)
        search_criteria = {
            "member": {"$in": [name]}
        }
        event_data = [
            event
            for event in get_user_events(search_criteria)
            if current_time > datetime.fromisoformat(event["date_end"])
        ]

        return render_template("home.html",
                               username = name, 
                               events = event_data,
                               level = level)
    else :
        return redirect(url_for('sign.index'))
    
@event_list_bp.route("/my_event")#自己創的活動
def my_event():
    if "username" in session:
        name = session["username"]
        level = find_user_level(name)
        search_criteria = {
            "host" : name
        } #找出主辦人有此user的活動
        event_data = get_user_events(search_criteria)

        return render_template("home.html",
                               username = name, 
                               events = event_data,
                               level = level)
    else :
        return redirect("/error")