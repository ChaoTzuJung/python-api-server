# 處理 user 所有資源操作 - CRUD
from flask_result import Response
import pymysql
# 建立 user 物件
class Users():
    def db_init(self):
        # 連結料庫
        db = pymysql.connect('localhost', 'root', 'password', 'api')
        # DictCursor 幫我們取資料時，把DB資料變成 key-value (1, 'John') -> {'id': 1, 'name': 'John'}
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor