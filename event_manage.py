from sign import *
from account_manage import *
from event_list import *

@app.route("/event/<event_id>")
def event(event_id):
    #print(event_id)
    collection = db["events"]
    table =  collection.find_one({
        "_id" : ObjectId(event_id) 
    })
    if table == None:
        return redirect("/error")
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

@app.route("/register_event/<event_id>")
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
        return redirect("/error")
    
@app.route("/create")
def create():
    return render_template("create_event.html") 

@app.route("/create_event",methods=["POST"])
def create_event():
    if "username" in session:
        title = request.form["title"]
        date_begin = request.form["date_begin"]
        date_begin = date_begin.replace("T","  ") 
        date_end = request.form["date_end"]
        date_end = date_begin.replace("T","   ")
        location = request.form["location"]
        limit_value = int(request.form["limit_value"])
        description = request.form["description"]
        host = session["username"]
        member = request.form.getlist("member")[:limit_value]

        #member = request.form["member"]
        #tag = request.form["tag"]
        #requirement = request.form["requirement"]
        collection = db["events"]
        result = collection.insert_one({
            "title":title,
            "date_begin":date_begin,
            "date_end":date_end,
            "location":location,
            "description":description,
            "host":host,
            "member":member,
            "limit_value":limit_value
            #"tag":tag,
            #"requirement":requirement,
        })
        if result.acknowledged:
            return {'result' : 'Success'}
        else:
            {'result' : 'Faliure'}
    else:
        return redirect("/error")

@app.route("/search_event", methods = ["POST"])
def search_event():
    name = session["username"]
    event_name = request.form["q"]
    collection = db["events"]
    result = collection.find_one({
        "title": { "$regex": event_name }
    })
    if result == None:
        return redirect("/error?msg=找不到此活動")
    num = 0
    result = collection.find({
        "title": { "$regex": event_name }
    })
    event = []
    event_id= []
    for doc in result:
        num += 1
        event_id.append(str(doc["_id"]))
        event.append(doc["title"])
    return render_template("home.html", username = name, title = event, num = num , _id = event_id)

@app.route("/delete_event/<event_id>")
def delete_event(event_id):
    if "username" in session:
        collection = db["events"]
        target = collection.find_one({
            "_id" : ObjectId(event_id) 
        })
        if target != None:
            collection.delete_one({
                "_id" : ObjectId(event_id) 
            })
            return {'result' : 'Success'}
        return {'result' : 'Notfind'}
    else :
        return redirect("/error")