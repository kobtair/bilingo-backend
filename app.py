from flask import Flask, request
app = Flask(__name__)
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

load_dotenv()

uri = os.getenv("MONGODB_URI")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app.config["DEBUG"] = True # Only include this while you are testing your app

db = client['bilingo']

user_collection = db['users']

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data:
        return 'No data received', 400
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return 'Email or Password is missing', 400
    current_user = user_collection.find_one({'email': email})
    if email == current_user.email and password == current_user.password:
        return 'Login Success'
    else:
        return 'Login Failed', 401
    
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data:
        return 'No data received', 400
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return 'Username or Password is missing', 400
    return 'User Registered Successfully'

if __name__ == '__main__':
    app.run()

