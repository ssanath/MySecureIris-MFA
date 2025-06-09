import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # Loads the .env file

MONGO_URI = os.getenv("mongodb+srv://sanath:apr26@cluster0.zst7rqb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
client = MongoClient(MONGO_URI)
db = client['secureiris']  # You can use any DB name here
