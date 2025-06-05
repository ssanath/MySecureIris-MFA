# user_model.py - base file
# user_model.py — MongoDB user schema + dummy insert

from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
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
