from flask import Flask, request, jsonify
from flask_restful import Api
from resources.user import Users, User
from resources.account import Accounts, Account
import pymysql
import traceback
import jwt
import time

# 宣告是 flask app
app = Flask(__name__) 
# 這是 api server
api = Api(app)

# 產生路由 - 進 /users 執行 Users 物件
api.add_resource(Users, '/users')
api.add_resource(User, '/user/<id>')
# Nest Resource 當一個資源是差在另一個資源下
api.add_resource(Accounts, '/user/<user_id>/accounts')
api.add_resource(Account, '/user/<user_id>/account/<id>')

@app.before_request()
def auth():
    token = request.headers.get('auth')
    user_id = request.get_json()['user_id']
    # 用 jwt 確認會員登入，用 user_id 與 timestamp 加密，在用 utf-8 解碼取得 token
    valid_token = jwt.encode({'user_id': user_id, 'timestamp': int(time.time())}, 'password', algorithm='HS256').decode('utf-8')
    print(valid_token)
    if token == valid_token:
        pass
    else:
        return {
            'msg': 'invalid token'
        }


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


