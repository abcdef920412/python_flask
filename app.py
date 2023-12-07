from flask import*
from flask import Flask
from sign import sign_bp
from event_manage import event_manage_bp
from event_list import event_list_bp
from account_manage import account_manage_bp

app = Flask(
    __name__,
    static_folder = "static",
    static_url_path = '/'
)
app.secret_key = "any"

# 註冊 Blueprint
app.register_blueprint(sign_bp, url_prefix='/sign')
app.register_blueprint(event_manage_bp, url_prefix='/event_manage')
app.register_blueprint(event_list_bp, url_prefix='/event_list')
app.register_blueprint(account_manage_bp, url_prefix='/account_manage')

# 重新定向根路徑到 sign_bp 藍圖的根路徑
@app.route('/')
def redirect_to_sign():
    return redirect(url_for('sign.index')) #檔名.

if __name__ == '__main__':
    app.run(port=3000)

# @app.route("/")
# def index():
#     return render_template("signin.html")

# @app.route("/sign")
# def sign():
#    return render_template("signup.html")
   
# @app.route("/member")
# def member():
#     if "username" in session:
#             collection = db["events"]
#             name = session["username"]
#             cursor = collection.find()
#             event = []
#             event_id = []
#             num = 0
#             for doc in cursor:
#                 event.append(doc["title"])
#                 event_id.append(str(doc["_id"]))
#                 num += 1
#             return render_template("home.html", username = name, title = event, _id = event_id, num = num)
#     else :
#         return redirect("/")
    
# @app.route("/event/<event_id>")
# def event(event_id):
#     #print(event_id)
#     collection = db["events"]
#     table =  collection.find_one({
#         "_id" : ObjectId(event_id) 
#     })
#     if table == None:
#         return redirect("/error?404")
#     title = table["title"]
#     date_begin = table["date_begin"]
#     date_end = table["date_end"]
#     location = table["location"]
#     description = table["description"]
#     limit_value = table["limit_value"]
#     registered_count = len(table["member"])
#     return render_template("event.html",
#                            event_id = event_id, 
#                            event_title = title, 
#                            date_begin = date_begin, 
#                            date_end = date_end , 
#                            event_location = location, 
#                            event_description = description,
#                            limit_value = limit_value,
#                            registered_count = registered_count
#                            )

# @app.route("/register_event/<event_id>")
# def register_event(event_id):
#     if "username" in session:
#         username = session["username"]
#         collection = db["events"]
#         filter = {"_id" : ObjectId(event_id)}
#         table = collection.find_one(filter)
#         if username not in table["member"]:
#             limit = table["limit_value"]
#             registered_count = len(table["member"])
#             if limit > registered_count:
#                 newvalue = {"$push": {"member": username}}
#                 collection.update_one(filter, newvalue)
#                 return {'result' : 'Success'}
#             else:
#                 return {'result' : 'isFull'}
#         return {'result' : 'isRegistered'}
#     else:
#         return redirect("/error")

# @app.route("/error")
# def error():
#     message=request.args.get("msg" , "發生錯誤")
#     return render_template("error.html",message=message)

# @app.route("/signup", methods = ["POST"])
# def signup():
#     fullname = request.form["fullname"]
#     username = request.form["username"]
#     password = request.form["password"]
#     identity = request.form["identity"]
#     comfirm_password = request.form["comfirm_password"]
#     identity=request.form["identity"]
#     #資料庫互動
#     if comfirm_password != password :
#        return redirect("/error?msg=確認密碼與密碼不符")
#     collection = db["users"]
#     result = collection.find_one({ 
#         "username": username
#     })
#     if result != None:
#         return redirect("/error?msg=帳號已被註冊過，請嘗試別的帳號")
#     collection.insert_one({
#         "fullname":fullname,
#         "username": username,
#         "password":password,
#         "identity":identity,
#         "level":"normal",
#     })
#     return redirect("/")

# @app.route("/signin",methods = ["POST"])
# def signin():
#     username = request.form["username"]
#     password = request.form["password"]
#     #資料庫互動
#     collection = db["users"]
#     result = collection.find_one({
#         "$and" :[
#             {"username":username, 
#              "password":password}
#         ]
#     })
#     if result == None:
#         return redirect("/error?msg=帳號密碼輸入錯誤")
#     session["username"] = result["username"]
#     return redirect("/member")

# @app.route("/signout")
# def signout():
#    del session["username"]
#    return redirect("/")

# @app.route("/create")
# def create():
#    return render_template("create_event.html")

# @app.route("/create_event",methods=["POST"])
# def create_event():
#     if "username" in session:
#         title = request.form["title"]
#         date_begin = request.form["date_begin"]
#         date_begin = date_begin.replace("T","   ") 
#         date_end = request.form["date_end"]
#         date_end = date_begin.replace("T","   ")
#         location = request.form["location"]
#         limit_value = int(request.form["limit_value"])
#         description = request.form["description"]
#         host = session["username"]
#         member = request.form.getlist("member")[:limit_value]

#         #member = request.form["member"]
#         #tag = request.form["tag"]
#         #requirement = request.form["requirement"]
#         collection = db["events"]
#         result = collection.insert_one({
#             "title":title,
#             "date_begin":date_begin,
#             "date_end":date_end,
#             "location":location,
#             "description":description,
#             "host":host,
#             "member":member,
#             "limit_value":limit_value
#             #"tag":tag,
#             #"requirement":requirement,
#         })
#         if result.acknowledged:
#             return {'result' : 'Success'}
#         else:
#             {'result' : 'Faliure'}
#     else:
#         return redirect("/error")

# @app.route("/search_event", methods = ["POST"])
# def search_event():
#     name = session["username"]
#     event_name = request.form["q"]
#     collection = db["events"]
#     result = collection.find_one({
#         "title": { "$regex": event_name }
#     })
#     if result == None:
#         return redirect("/error?msg=找不到此活動")
#     num = 0
#     result = collection.find({
#         "title": { "$regex": event_name }
#     })
#     event = []
#     event_id= []
#     for doc in result:
#         num += 1
#         event_id.append(str(doc["_id"]))
#         event.append(doc["title"])
#     return render_template("home.html", username = name, title = event, num = num , _id = event_id)

# @app.route("/delete_event/<event_id>")
# def delete_event(event_id):
#     if "username" in session:
#         collection = db["events"]
#         filter = {"_id" : ObjectId(event_id)}
#         target = collection.find_one(filter)
#         if target != None:
#             collection.delete_one(filter)
#             return {'result' : 'Success'}
#         return {'result' : 'Notfind'}
#     else :
#         return redirect("/error")

# @app.route("/attend_event")#自己有報名的活動
# def attend_event():
#     if "username" in session:
#         collection = db["events"]
#         name = session["username"]
#         result = collection.find({#找出成員內有此user的活動
#             "member" : name
#         })
#         event = []
#         for doc in result:
#             event.append(doc["title"])
#         return render_template("home.html", username = name, title = event)
#     else :
#         return redirect("/error")

# @app.route("/my_event")#自己創的活動
# def my_event():
#     if "username" in session:
#         collection = db["events"]
#         name = session["username"]
#         result = collection.find({#找出主辦人有此user的活動
#             "host" : name
#         })
#         event = []
#         for doc in result:
#             event.append(doc["title"])
#         return render_template("home.html", username = name, title = event)
#     else :
#         return redirect("/error")
    
# @app.route("/end_event")#自己有參加(報名)且已結束的活動
# def end_event():
#     if "username" in session:
#         collection = db["events"]
#         name = session["username"]
#         rightnow = datetime.now()#有import
#         result = collection.find({#找出成員或主持內有此user且已過期的活動
#             "$and" :[{
#                 {"date" : {"$lte" : rightnow}},
#                 {"$or" : [
#                     {"member" : name},
#                     {"host" : name}
#                 ]}
#             }]
#         })
#         event = []
#         for doc in result:
#             event.append(doc["title"])
#         return render_template("home.html", username = name, title = event)
#     else :
#         return redirect("/error")

# ... （其他代码）


