from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
# 連結資料庫  'mysql+pymysql://帳號:密碼@本地PORT/api'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/api'
db = SQLAlchemy(app)
