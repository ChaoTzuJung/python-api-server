import requests
import json
import jwt
import time

url = "http://0.0.0.0:5000/users"

payload = "{\"user_id\": \"123\"}"
# 函式 time() ，是用來獲取如 1592664946 的時間戳記值， time.time() 回傳的是 float。
valid_token = jwt.encode({'user_id': '123', 'timestamp': int(time.time())}, 'password', algorithm='HS256').decode('utf-8')
headers = {
    'Content-Type': 'application/json',
    'auth': valid_token
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
