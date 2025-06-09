# user_model.py - base file
# user_model.py — MongoDB user schema + dummy insert

from pymongo import MongoClient
import os

# Connect to MongoDB
MONGO_URI = os.getenv("mongodb+srv://sanath:apr26@cluster0.zst7rqb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
client = MongoClient(MONGO_URI)
db = client["secure_iris"]
users_collection = db["users"]

# Dummy user insert function
def insert_dummy_user():
    dummy_user = {
        "user_id": "user001",
        "email": "test@example.com",
        "password": "hashed_password",
        "iris": None
    }
    if not users_collection.find_one({"email": dummy_user["email"]}):
        users_collection.insert_one(dummy_user)
        print("✅ Dummy user inserted")
    else:
        print("⚠️ Dummy user already exists")
