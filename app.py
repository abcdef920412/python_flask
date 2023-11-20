from flask import*
import pymongo 
uri = "mongodb+srv://root:root920412@cluster0.lvs2gvu.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)

db = client.member_system

app = Flask(
    __name__,
    static_folder = "static",
    static_url_path = '/'
)
app.secret_key = "any"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sign")
def sign():
   return render_template("signup.html")
   
@app.route("/member")
def member():
    if "username" in session:
            collection = db["events"]
            name = session["username"]
            cursor = collection.find()
            event = []
            for doc in cursor:
                event.append(doc["title"])
            return render_template("member.html", username = name, title = event)
    else :
        return redirect("/")
@app.route("/error")
def error():
    message=request.args.get("msg" , "發生錯誤")
    return render_template("error.html",message=message)

@app.route("/signup", methods = ["POST"])
def signup():
    fullname = request.form["fullname"]
    username = request.form["username"]
    password = request.form["password"]
    comfirm_password = request.form["comfirm_password"]
    #資料庫互動
    if comfirm_password != password :
       return redirect("/error?msg=確認密碼與密碼不符")
    collection = db["users"]
    # result = collection.find_one({ 
    #     "username": username
    # })
    # if result != None:
    #     return redirect("/error")
    collection.insert_one({
        "fullname":fullname,
        "username": username,
        "password":password,
        "level":"使用者",
        "identity":"老師"
    })
    return redirect("/")

@app.route("/signin",methods = ["POST"])
def signin():
    username = request.form["username"]
    password = request.form["password"]
    #資料庫互動
    collection = db["users"]
    result = collection.find_one({
        "$and" :[
            {"username":username, 
             "password":password}
        ]
    })
    if result == None:
        return redirect("/error?msg=帳號密碼輸入錯誤")
    session["username"] = result["username"]
    return redirect("/member")

@app.route("/signout")
def signout():
   del session["username"]
   return redirect("/")

@app.route("/create")
def create():
   return render_template("create_event.html")

@app.route("/create_event",methods=["POST"])
def create_event():
   title = request.form["title"]
   date = request.form["date"]
   location = request.form["location"]
   description = request.form["description"]
   collection = db["events"]
   collection.insert_one({
      "title":title,
      "date":date,
      "location":location,
      "description":description,
   })
   return redirect("/create")

@app.route("/search_event", methods = ["POST"])
def search_event():
    event_name = request.form["q"]
    collection = db["events"]
    result = collection.find_one({
        "title": { "$regex": event_name }
    })
    if result == None:
        return redirect("/error")
    result = collection.find({
        "title": { "$regex": event_name }
    })
    for doc in result:
        print(doc)
    return redirect("/create")

app.run(port = 3000)
