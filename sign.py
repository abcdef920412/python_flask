from flask import Blueprint, render_template, redirect, url_for, request, session
from db_conn import db

sign_bp = Blueprint('sign', __name__)

@sign_bp.route("/")
def index():
    return render_template("signin.html")

@sign_bp.route("/error")
def err():
    message=request.args.get("msg" , "發生錯誤")
    return render_template("error.html", message=message)

@sign_bp.route("/sign")
def sign():
   return render_template("signup.html")

@sign_bp.route("/signup", methods = ["POST"])
def signup():
    fullname = request.form["fullname"]
    username = request.form["username"]
    password = request.form["password"]
    identity = request.form["identity"]
    comfirm_password = request.form["comfirm_password"]
    identity=request.form["identity"]
    #資料庫互動
    if comfirm_password != password :
       return redirect(url_for('sign.err'))
    collection = db["users"]
    result = collection.find_one({ 
        "username": username
    })
    if result != None:
        return redirect(url_for('sign.err'))
    collection.insert_one({
        "fullname":fullname,
        "username": username,
        "password":password,
        "identity":identity,
        "level":"normal",
        "isban":False
    })
    return redirect(url_for('sign.index')) # 使用 url_for 生成 /sign 路由的 URL，然後進行重定向

@sign_bp.route("/signin",methods=["GET", "POST"])
def signin():
    username = request.form["username"]
    password = request.form["password"]
    #資料庫互動
    collection = db["users"]
    result = collection.find_one({
        "$and" :[
            {"username":username, 
             "password":password,
             "isban":False}
        ]
    })
    if result == None:
        return redirect(url_for('sign.err'))
    session["username"] = result["username"]
    #print(session)
    return redirect(url_for('event_manage.member'))

@sign_bp.route("/signout")
def signout():
   del session["username"]
   return redirect(url_for('sign.index'))