from flask import Flask
from flask_result import Api
from resources.user import Users

# 宣告是 flask app
app = Flask(__name__) 
# 這是 api server
api = Api(app)

# 產生路由 - 進 /users 執行 Users 物件
api.add_resource(Users, '/users')

@app.route('/')
def index():
    return 'Hello World'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


