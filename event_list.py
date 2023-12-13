from sign import *
from event_manage import *
from account_manage import *

@app.route("/member")
def member():
    if "username" in session:
            collection = db["events"]
            name = session["username"]
            cursor = collection.find()
            event = []
            event_id = []
            num = 0
            for doc in cursor:
                event.append(doc["title"])
                event_id.append(str(doc["_id"]))
                num += 1
            return render_template("home.html", username = name, title = event, _id = event_id, num = num)
    else :
        return redirect("/")
    
@app.route("/attend_event")#自己有報名的活動
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
    
@app.route("/my_event")#自己創的活動
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

@app.route("/end_event")#自己有參加(報名)且已結束的活動
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