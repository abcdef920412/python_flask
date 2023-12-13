from sign import *
from event_manage import *
from event_list import *
"""@app.route("/permission")
def permission_adjust():
    command = request.form["command"]
    collection = db["users"]
    if command == "加入黑名單":

        for name in username:
            collection.find({
                "username":username,
            })
    elif command == "移除黑名單":

    elif command == "設定為進階使用者":

    elif command == "設定為一般使用者":

    return render_template("userdata.html")"""