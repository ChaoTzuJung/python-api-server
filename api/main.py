from flask import Flask, request, jsonify
from flask_restful import Api
from resources.user import Users, User
from resources.account import Accounts, Account
import pymysql
import traceback
import jwt
import time
from server import app

# 宣告是 flask app，__name__ 是 python 中，讓同層的其他檔案，可以成為讓其他 python 檔案使用的 module ，所需要的預設檔案。
app = Flask(__name__) 
# 這是 api server
api = Api(app)

# 產生路由 - 進 /users 執行 Users 物件
api.add_resource(Users, '/users')
api.add_resource(User, '/user/<id>')
# Nest Resource 當一個資源是差在另一個資源下
api.add_resource(Accounts, '/user/<user_id>/accounts')
api.add_resource(Account, '/user/<user_id>/account/<id>')

# Flask 中發生錯誤都會進來此函式
@app.errorhandler(Exception)
def handle_error(error):
    status_code = 500
    # 可以知道此類別的 class 是什麼
    if type(error).__name__ == 'NotFound':
        status_code = 404
    elif type(error).__name__ == 'TypeError':
        status_code = 500

    return jsonify({'msg': type(error).__name__}), status_code

# 讀所有端點都要先經過驗證
# @app.before_request
# def auth():
#     #檢查 header 有無token
#     token = request.headers.get('auth')
#     # 用 json 方式傳 user_id
#     user_id = request.get_json()['user_id']
#     # 用 jwt 確認會員登入，用 user_id 與 timestamp 加密，在用 utf-8 解碼取得 token
#     # jwt.encode('要加密的資料', secert_key, '使用的演算法')
#     # jwt.decode('使用的解碼方式') 
#     valid_token = jwt.encode({'user_id': user_id, 'timestamp': int(time.time())}, 'password', algorithm='HS256').decode('utf-8')
#     print(valid_token)
#     if token == valid_token:
#         pass
#     else:
#         return {
#             'msg': 'invalid token'
#         }


# @裝飾子
@app.route('/')
def index():
    return 'Hello World'

# 客製化路徑名稱 Ex: 
@app.route('/user/<user_id>/account/<id>/deposit', methods=['POST'])
# 為此路徑新增函示
def deposit(user_id, id):
    db, cursor, account = get_account(id)
    money = request.get_json()['money']
    balance = account['balance'] + int(money)
    sql = """
        UPDATE `api`.`accounts` SET balance = '{}' where id = '{}' and deleted is NOT True
    """.format(balance, id)
    response = {}
    try:
        cursor.execute(sql)
        response['msg'] = 'success'
    except:
        traceback.print_exc()
        response['msg'] = 'failed'
    db.commit()
    db.close()

    return jsonify(response)

@app.route('/user/<user_id>/account/<id>/withdraw', methods=['POST'])
def withdraw(user_id, id):
    db, cursor, account = get_account(id)
    money = request.get_json()['money']
    balance = account['balance'] - int(money)
    response = {}
    if balance < 0:
        response['msg'] = 'money not enough'
        return jsonify(response)
    else:
        sql = """
            UPDATE `api`.`accounts` SET balance = '{}' where id = '{}' and deleted is NOT True
        """.format(balance, id)
        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        db.commit()
        db.close()

        return jsonify(response)

def get_account(id):
    db = pymysql.connect('localhost', 'root', 'password', 'api')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = """Select * From api.accounts Where id = '{}' and deleted is not True """.format(id)
    cursor.execute(sql)
    # cursor.fetchone() --> 回傳sql執行後得到的acount物件
    return db, cursor, cursor.fetchone()

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


