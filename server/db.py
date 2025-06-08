import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # Loads the .env file

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['secureiris']  # You can use any DB name here
