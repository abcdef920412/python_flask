from flask import Blueprint, render_template, redirect, url_for, request, session
from bson import ObjectId
from datetime import datetime
from db_conn import db
from event_function import get_user_events, find_user_identity, find_user_level

event_manage_bp = Blueprint('event_manage', __name__)

@event_manage_bp.route("/guest")
def guest():
    if session.get("username"): # 如果有則刪除
        del session["username"]
    event_data = [
        event
        for event in get_user_events({}, True)
        for event in get_user_events("", {})
    ]

    return render_template("home.html",
                            username = "Guest", 
                            events = event_data,
                            level = "visitor")

@event_manage_bp.route("/member")
def member():
    if "username" in session:
        collection = db['users']
        name = session["username"]
        user = collection.find_one(
            {"username": name}
        )
        event_data = [
        event
        for event in get_user_events(name, {})
        ]

        return render_template("home.html",
                               username = name, 
                               events = event_data,
                               level = user["level"])
    else :
        #return redirect(url_for('sign.index'))
        return guest()

@event_manage_bp.route("/event/<event_id>")#顯示活動資訊
def event(event_id):
    collection = db["events"]
    table =  collection.find_one({
            "_id" : ObjectId(event_id) 
        })
    if table == None:
        return redirect(url_for('event_manage.member'))
    member = []
    if "username" in session : #登入狀態
        #print(event_id)
        collection1 = db['users']
        name = session["username"]
        user = collection1.find_one(
            {"username": name}
        )
        #只有系統管理員或該活動主辦人可調閱 member 資料
        level = user["level"]
        if level == "advanced" or name == table["host"]: 
            member = table["member"]
    else:
        name = "Guest"
        level = "visitor"
    #print(name, level)

    event_data = [{
        "title": table["title"],
        "host": table["host"],
        "date_begin": table["date_begin"],
        "date_end": table["date_end"],
        "location": table["location"],
        "description": table["description"],
        "limit_value": table["limit_value"],
        "registered_count": len(table["member"]),
        "organizing_group": table["tag"][0],
        "activity_type": table["tag"][1],
        }]
    return render_template("event.html",
                           name = name,
                           events = event_data,
                           event_id = event_id,
                           level = level,
                           host = table["host"],
                           members = member)

@event_manage_bp.route("/register_event/<event_id>")#報名活動
def register_event(event_id):
    if "username" in session:
        username = session["username"]
        collection = db["events"]
        filter = {"_id" : ObjectId(event_id)}
        event = collection.find_one(filter)
        if datetime.now() > datetime.fromisoformat(event["date_end"]):
            return {'result' : 'registrationClosed'}
        if event["requirement"] not in [find_user_identity(username), "all"]:
            return {'result' : 'invalid_identity'}
        if username not in event["member"]:
            limit = event["limit_value"]
            registered_count = len(event["member"])
            if limit > registered_count:
                newvalue = {"$push": {"member": username}}
                collection.update_one(filter, newvalue)
                return {'result' : 'Success'}
            else:
                return {'result' : 'isFull'}
        return {'result' : 'isRegistered'}
    else:
        return redirect(url_for('sign.index'))

@event_manage_bp.route("/error")
def error():
    message=request.args.get("msg" , "發生錯誤")
    return render_template("error.html", message=message)

@event_manage_bp.route("/create")
def create():
   return render_template("create_event.html")

@event_manage_bp.route("/create_event", methods=["POST"])
def create_event():
    if "username" in session:
        if find_user_level(session["username"]) not in ["advanced", "admin"]:
            return {'result' : 'UnAuthorized'}
        title = request.form["title"]
        date_begin = request.form["date_begin"]
        date_end = request.form["date_end"]
        location = request.form["location"]
        limit_value = int(request.form["limit_value"])
        description = request.form["description"]
        organizing_group = request.form["organizing_group"]
        activity_type = request.form["activity_type"]
        requirement = request.form["identity"]
        host = session["username"]
        member = request.form.getlist("member")[:limit_value]
        tag_values = [organizing_group, activity_type] # 根據設計文件皆為 tag
        
        collection = db["events"]
        result = collection.insert_one({
            "title":title,
            "date_begin":date_begin,
            "date_end":date_end,
            "location":location,
            "description":description,
            "host":host,
            "member":member,
            "limit_value":limit_value,
            "tag":tag_values,
            "requirement":requirement
        })
        if result.acknowledged:
            return {'result' : 'Success'}
        else:
            return {'result' : 'Faliure'}
    else:
        return redirect(url_for('sign.index'))

@event_manage_bp.route("/search_event", methods = ["POST"])
def search_event():
    if session.get("username"):
        name = session["username"]
    else:
        name = ""
    event_name = request.form["q"]
    """可以收進階搜尋
    for wtffff in wtf:
        print(wtffff)
    """
    filter_value = request.form["filter"]
    # 初始化 search_criteria，設置通用條件
    search_criteria = {
        "title": {"$regex": event_name}
    }

    # 根據不同的 filter 值修改 search_criteria
    if filter_value == "attend" or filter_value == "myend":
        search_criteria["member"] = {"$in": [name]}
    elif filter_value == "joinable":
        identity = find_user_identity(name)
        search_criteria.update({ #未報名且符合資格
        "$and": [
            {"member": {"$nin": [name]}},
            {"requirement": {"$in": [identity, "all"]}}
        ]})
    elif filter_value == "my":
        search_criteria["host"] = name

    event_data = get_user_events(name, search_criteria)

    if not event_data: # 因為關鍵字而導致的 notFind
        return {
            "result": "notFind",
            "events": ""
        }
    current_time = datetime.now()
    if filter_value == "myend" or filter_value == "end":
        event_data = [
            event
            for event in event_data
            if current_time > datetime.fromisoformat(event["date_end"])
        ]
    elif filter_value == "attend" or filter_value == "joinable":
        event_data = [
            event
            for event in event_data
            if current_time <= datetime.fromisoformat(event["date_end"])
        ]
    if not event_data: # 因為時間限制而導致的 notFind
        return {
            "result": "notFind",
            "events": ""
        }
    return {
        "result": "Find",
        "events": event_data
    }

@event_manage_bp.route("/delete_event/<event_id>")
def delete_event(event_id):
    if "username" in session:
        if find_user_level(session["username"]) not in ["advanced", "admin"]:
            return redirect(url_for('sign.index'))
        collection = db["events"]
        filter = {"_id" : ObjectId(event_id)}
        target = collection.find_one(filter)
        if target != None:
            if target["host"] != session["username"]:
                return {'result' : 'UnAuthorized'}
            collection.delete_one(filter)
            return {'result' : 'Success'}
        return {'result' : 'Notfound'}
    else :
        return redirect(url_for('sign.index'))
    
@event_manage_bp.route("/applicant/<event_id>")
def find_member(event_id):
    if "username" in session:
        collection = db["events"]
        filter = {"_id" : ObjectId(event_id)}
        target = collection.find_one(filter)
        if target != None:
            return target["member"]#誰接
        return {'result' : 'Notfound'}
    else :
        return redirect(url_for('sign.index'))