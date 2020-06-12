# 處理 user 所有資源操作 - CRUD
from flask_restful import Resource, reqparse
from flask import jsonify
# 幫助 python 連結到 mysql
import pymysql
# 印出錯誤訊息的套件
import traceback

# 幫我們處理使用者傳的參數
parser = reqparse.RequestParser()
# 設定白名單，哪些參數要接，讓 arg 可以讀取 url 給的query參數
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')

class User(Resource):
    # 執行db_init() 就可以拿到資料庫初始的 db 與 cursor
    def db_init(self):
        # 'localhost', 'root', '你自訂的資料庫密碼', 'schema 名稱'
        db = pymysql.connect('localhost', 'root', 'password', 'api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self, id):
        db, cursor = self.db_init()
        sql = """Select * From api.users Where id = '{}' and deleted is not True """.format(id)
        cursor.execute(sql)
        # db 確認好就送出
        db.commit()
        # 取得 cursor 所有資料
        user = cursor.fetchone()
        db.close()
        return jsonify({ 'data': user })

    def patch(self, id):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        user = {
            'name': arg['name'],
            'gender': arg['gender'],
            'birth': arg['birth'],
            'note': arg['note'],
        }
        query = []
        for key, value in user.items():
            if value != None:
                query.append(key + " = " + "'{}'".format(value))

        query = ', '.join(query)
        sql = """
            UPDATE `api`.`users` SET {} WHERE (`id` = '{}');
        """.format(query, id)
        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'fail'
        db.commit()
        db.close()
        return jsonify(response)
    def delete(self, id):
        db, cursor = self.db_init()
        sql = """
            UPDATE `api`.`users` SET deleted = True WHERE (`id` = '{}');
        """.format(id)
        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'fail'
        db.commit()
        db.close()
        return jsonify(response)

# 建立 users 物件, self 就是 this，資源初始化設定
class Users(Resource):
    def db_init(self):
        # 連結料庫
        db = pymysql.connect('localhost', 'root', 'password', 'api')
        # DictCursor 幫我們取資料時，把DB資料變成 key-value (1, 'John') -> {'id': 1, 'name': 'John'}
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    # http get method
    def get(self):
        db, cursor = self.db_init()
        # schema.table 
        sql = 'Select * From api.users where deleted is not True'
        arg = parser.parse_args()
        if arg['gender'] != None:
            sql += ' and gender = "{}"'.format(arg['gender'])
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
        arg = parser.parse_args()
        user = {
            'name': arg['name'],
            'gender': arg['gender'] or 0,
            'birth': arg['birth'] or '1900-01-01',
            'note': arg['note'],
        }
        # 3個引號讓 python 知道這是長字串，換行時python不會把字串當成新的一行
        sql = """
            INSERT INTO `api`.`users` (`name`, `gender`, `birth`, `note`) VALUES ('{}', '{}', '{}', '{}');
        """.format(user['name'], user['gender'], user['birth'], user['note'])

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