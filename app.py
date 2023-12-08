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
    return redirect(url_for('sign.index'))

if __name__ == '__main__':
    app.run(port=3000)

"""@app.route("/permission")
def permission_adjust():
    command = request.form["command"]
    target = request.form["user"]
    collection = db["users"]
    if command == "加入黑名單":

        for name in username:
            result = collection.find({
                "username":username,
            })
        for doc in result:
            collection.update_many({
                {"username" : target}, {"$set" : "isban" = true}
            })
                
    elif command == "移除黑名單":

        for name in username:
            result = collection.find({
                "username":username,
            })
        for doc in result:
            collection.update_many({
                {"username" : target}, {"$set" : "isban" = false}
            })
                
    elif command == "設定為進階使用者":

        for name in username:
            result = collection.find({
                "username":username,
            })
        for doc in result:
            collection.update_many({
                {"username" : target}, {"$set" : "level" = "advanced"}
            })
                
    elif command == "設定為一般使用者":

        for name in username:
            result = collection.find({
                "username":username,
            })
        for doc in result:
            collection.update_many({
                {"username" : target}, {"$set" : "level" = "normal"}
            })
                
    return render_template("userdata.html")"""
