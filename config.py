from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

load_dotenv()

uri = os.getenv("MONGODB_URI")
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['bilingo']
user_collection = db['users']
course_collection = db['courses']
audio_collection = db['audioFiles']
admin_collection = db['admins']
chapter_collection = db['chapters']