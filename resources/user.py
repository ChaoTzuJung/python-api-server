# 處理 user 所有資源操作 - CRUD
from flask_result import Response, reqparse
from flask import jsonify
import pymysql
# 印出錯誤訊息
import traceback

# 幫我們處理使用者傳的參數
parser = reqparse.RequestParser()
# 設定白名單，哪些參數要接
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')

# 建立 user 物件, self 就是 this
class Users():
    def db_init(self):
        # 連結料庫
        db = pymysql.connect('localhost', 'root', 'password', 'api')
        # DictCursor 幫我們取資料時，把DB資料變成 key-value (1, 'John') -> {'id': 1, 'name': 'John'}
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    # http get method
    def get(self):
        db, cursor = self.db_init()
        sql = 'Select * From api.users'
        cursor.execute(sql)
        # db 確認好就送出
        db.commit()
        # 取得 cursor 所有資料
        users = cursor.fetchall()
        db.close()

        return jsonify({ 'data': users })
    def post(self):
        db, cursor = self.db_init()
        # 把使用者給我的參數傳到 arg 內
        arg = parser.parser_args()
        user = {
            'name': arg['name'],
            'gender': arg['gender'] or 0,
            'birth': arg['birth'] or '1900-01-01',
            'note': arg['note'],
        }
        # 讓 python 知道這是長字串  
        sql = """
            INSERT INTO `api`.`users` (`id`, `name`, `gender`, `birth`, `note`) VALUES ('{}', '{}', '{}', '{}', '{}');
        """.format(user['name'], user['gender'], user['birth'], user['note'])

        try
            cursor.execute(sql)
            response['msg'] = 'success'
        except expression as identifier:
            traceback.print_exc()
            response['msg'] = 'failed'
        db.commit()
        db.close()
        return jsonify(response)