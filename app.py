from flask import Flask, request
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import bcrypt

load_dotenv()

app = Flask(__name__)

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
    print("data", data)
    if not data:
        return 'No data received', 400
    email = data.get('email')
    password = data.get('password')
    bytes = password.encode('utf-8')
    if not email or not password:
        return 'Email or Password is missing', 400
    current_user = user_collection.find_one({'email': email})
    print("current_user", current_user)
    if email == current_user["email"] and bcrypt.checkpw(bytes, current_user["password"]):
        return 'Login Success'
    else:
        return 'Login Failed', 401
    
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data:
        return 'No data received', 400
    email = data.get('email')
    password = data.get('password')
    bytes = password.encode('utf-8') 
    salt = bcrypt.gensalt() 
    hash = bcrypt.hashpw(bytes, salt)
    if not email or not password:
        return 'Email or Password is missing', 400
    if '@' not in email:
        return 'Invalid Email', 400
    if len(password) < 6:
        return 'Password is too short', 400
    user_collection.insert_one({
        'email': email,
        'password': hash
    })
    return 'User Registered Successfully'

if __name__ == '__main__':
    app.run()

