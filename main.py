from flask import Flask
from flask_restful import Api
from resources.user import Users, User

# 宣告是 flask app
app = Flask(__name__) 
# 這是 api server
api = Api(app)

# 產生路由 - 進 /users 執行 Users 物件
api.add_resource(Users, '/users')
api.add_resource(User, '/user/<id>')

# @裝飾子
@app.route('/')
def index():
    return 'Hello World'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


