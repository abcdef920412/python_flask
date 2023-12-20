from flask import Blueprint, render_template, redirect, url_for, request, session
from bson import ObjectId
from db_conn import db

event_manage_bp = Blueprint('event_manage', __name__)

@event_manage_bp.route("/guest")
def guest():        
    collection = db["events"]
    user_events = collection.find({})
    event_data = [{
    "_id": str(event["_id"]),
    "title": event["title"],
    "host": event["host"],
    "date_begin": event["date_begin"].split("T")[0], #取年月日
    "date_end": event["date_end"].split("T")[0],
    "organizing_group": event["tag"][0],
    "activity_type": event["tag"][1],
    "registration_status": "未報名",
    "remaining_quota": event["limit_value"] - len(event["member"])
    } 
    for event in user_events]

    return render_template("home.html",
                            username = "Guest", 
                            events = event_data,
                            level = "visitor")

@event_manage_bp.route("/member")
def member():
    if "username" in session:
        collection = db["events"]
        collection1 = db['users']
        name = session["username"]
        users = collection1.find(
            {"username": name}
        )
        for doc in users:
            level = doc['level']
        user_events = collection.find({})
        event_data = [{
        "_id": str(event["_id"]),
        "title": event["title"],
        "host": event["host"],
        "date_begin": event["date_begin"].split("T")[0], #取年月日
        "date_end": event["date_end"].split("T")[0],
        "organizing_group": event["tag"][0],
        "activity_type": event["tag"][1],
        "registration_status": "已報名" if name in event["member"] else "未報名",
        "remaining_quota": event["limit_value"] - len(event["member"])
        } 
        for event in user_events]

        return render_template("home.html",
                               username = name, 
                               events = event_data,
                               level = level)
    else :
        #return redirect(url_for('sign.index'))
        return guest()

@event_manage_bp.route("/event/<event_id>")#顯示活動資訊
def event(event_id):
    #print(event_id)
    collection = db["events"]
    table =  collection.find_one({
        "_id" : ObjectId(event_id) 
    })
    if table == None:
        return redirect("/error?404")
    
    title = table["title"]
    date_begin = table["date_begin"]
    date_end = table["date_end"]
    location = table["location"]
    description = table["description"]
    limit_value = table["limit_value"]
    registered_count = len(table["member"])
    return render_template("event.html",
                           event_id = event_id, 
                           event_title = title, 
                           date_begin = date_begin, 
                           date_end = date_end , 
                           event_location = location, 
                           event_description = description,
                           limit_value = limit_value,
                           registered_count = registered_count
                           )

@event_manage_bp.route("/register_event/<event_id>")#報名活動
def register_event(event_id):
    if "username" in session:
        username = session["username"]
        collection = db["events"]
        filter = {"_id" : ObjectId(event_id)}
        table = collection.find_one(filter)
        if username not in table["member"]:
            limit = table["limit_value"]
            registered_count = len(table["member"])
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
    name = session["username"]
    event_name = request.form["q"]
    """可以收進階搜尋
    wtf = request.form.getlist("host_type")
    for wtffff in wtf:
        print(wtffff)
    """
    collection = db["events"]
    result = collection.find({
        "title": {"$regex": event_name}
    })
    event_data = [{
    "_id": str(event["_id"]),
    "title": event["title"],
    "host": event["host"],
    "date_begin": event["date_begin"].split("T")[0], #取年月日
    "date_end": event["date_end"].split("T")[0],
    "organizing_group": event["tag"][0],
    "activity_type": event["tag"][1],
    "registration_status": "已報名" if name in event["member"] else "未報名",
    "remaining_quota": event["limit_value"] - len(event["member"])
    } 
    for event in result]

    if not event_data:
        all_events = collection.find({})
        all_events_list = [{
        "_id": str(event["_id"]),
        "title": event["title"],
        "host": event["host"],
        "date_begin": event["date_begin"].split("T")[0], #取年月日
        "date_end": event["date_end"].split("T")[0],
        "organizing_group": event["tag"][0],
        "activity_type": event["tag"][1],
        "registration_status": "已報名" if name in event["member"] else "未報名",
        "remaining_quota": event["limit_value"] - len(event["member"])
        } 
        for event in all_events]

        return {
            "result": "notFind",
            "events": all_events_list
        }

    return {
        "result": "Find",
        "events": event_data
    }

@event_manage_bp.route("/delete_event/<event_id>")
def delete_event(event_id):
    if "username" in session:
        collection = db["events"]
        filter = {"_id" : ObjectId(event_id)}
        target = collection.find_one(filter)
        if target != None:
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