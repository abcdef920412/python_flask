from flask import Blueprint, render_template, redirect, request, session
from bson import ObjectId
from db_conn import db

account_manage_bp = Blueprint('account_manage', __name__)

@account_manage_bp.route("/permission")
def permission_adjust():
    command = request.form["command"]
    username = request.form["user"]
    collection = db["users"]
    if command == "加入黑名單":
        for name in username:
            result = collection.find({
                "username":username,
            })
        for doc in result:
            collection.update_many({
                {"username" : username}, 
                {"$set" : {"isban" : True}}
            })
    elif command == "移除黑名單":
        for name in username:
            result = collection.find({
                "username":username,
            })
        for doc in result:
            collection.update_many({
                {"username" : username},
                {"$set" : {"isban" : False}}
            })
    elif command == "設定為進階使用者":
        for name in username:
            result = collection.find({
                "username":username,
            })
        for doc in result:
            collection.update_many({
                {"username" : username},
                {"$set" : {"level" : "advanced"}}
            })         
    elif command == "設定為一般使用者":
        for name in username:
            result = collection.find({
                "username":username,
            })
        for doc in result:
            collection.update_many({
                {"username" : username},
                {"$set" : {"level" : "normal"}}
            })
    return render_template("userdata.html")