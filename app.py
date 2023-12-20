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
    return redirect(url_for('event_manage.guest'))

if __name__ == '__main__':
    app.run(port=3000)