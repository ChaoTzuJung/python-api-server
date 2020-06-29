# 建立資料庫模型
from server import db

class UserModel(db.Model):
    # 設定 table name連到哪個資料庫
    __tablename__ = 'users'
    print(db)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    gender = db.Column(db.Integer)
    birth = db.Column(db.DateTime)
    note = db.Column(db.Text)
    deleted = db.Column(db.Boolean)

    def __init__(self, name, gender, birth, note, deleted = None):
        self.name = name
        self.gender = gender
        self.birth = birth
        self.note = note
        self.deleted = deleted

    # 因為 API server 是回傳 json 格式，但user model 有自己的資料格式，所以我們要成 dictionary
    def serialize(self):
        return {
            "name": self.name,
            "gender": self.gender,
            "birth": self.birth,
            "note": self.note,
            "deleted": self.deleted,
        }
