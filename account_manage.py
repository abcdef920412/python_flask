from flask import Blueprint, render_template, redirect, request, session
from bson import ObjectId
from db_conn import db

account_manage_bp = Blueprint('account_manage', __name__)

@account_manage_bp.route("/users")
def getUserdata():
    collection = db["users"]
    cursor = collection.find()
    users = []
    for doc in cursor:
        users.append([doc["username"], doc["level"], doc["identity"], doc["isban"]])
    return render_template("userdata.html", users = users)

@account_manage_bp.route("/filter", methods=["POST"])
def search_user():
    username = request.form["query"]
    collection = db["users"]
    result = collection.find_one({
        "username": { "$regex": username }
    })
    if result == None:
        return redirect("/error?msg=找不到此使用者")
    result = collection.find({
        "username": { "$regex": username }
    })
    users = []
    for doc in result:
        users.append([doc["username"], doc["level"], doc["identity"], doc["isban"]])
    return render_template("userdata.html", users = users)

@account_manage_bp.route("/permission", methods=["POST"])
def permission_adjust():
    command = request.form["command"]
    username = request.form.getlist("user")

    for x in username:#test
        print(x)

    collection = db["users"]
    if command == "加入黑名單":
        newvalue = {"$set" : {"isban" : True}}
        for name in username:
            filter = {"username" : name}
            collection.update_one(filter, newvalue)
    elif command == "移除黑名單":
        newvalue = {"$set" : {"isban" : False}}
        for name in username:
            filter = {"username" : name}
            collection.update_one(filter, newvalue)
    elif command == "設定為進階使用者":
        newvalue = {"$set" : {"level" : "advanced"}}
        for name in username:
            """
            *** Problem : TypeError: Unhashable Type: 'Dict' ***
            collection.update_one({
                {"username" : name},
                {"$set" : {"level" : "advanced"}}
            }) """
            filter = {"username" : name}
            collection.update_one(filter, newvalue)
    elif command == "設定為一般使用者":
        newvalue = {"$set" : {"level" : "normal"}}
        for name in username:
            filter = {"username" : name}
            collection.update_one(filter, newvalue)
    cursor = collection.find()
    users = []
    for doc in cursor:
        users.append([doc["username"], doc["level"], doc["identity"], doc["isban"]])
    return render_template("userdata.html", users = users)