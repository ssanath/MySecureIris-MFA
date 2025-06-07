import os
import cv2
import base64
import numpy as np
import bcrypt
from flask import jsonify
from bson.objectid import ObjectId
from models.user_model import users_collection
from utils.otp_util import (
    generate_otp, send_otp_email, otp_store,
    get_otp_for, increment_attempt, reset_attempts
)

# Load Haar Cascade once
CASCADE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../utils/haarcascade_eye.xml"))
eye_cascade = cv2.CascadeClassifier(CASCADE_PATH)

# ------------------ Image Processing ------------------

def decode_image(b64_img):
    img_bytes = base64.b64decode(b64_img.split(",")[1])
    nparr = np.frombuffer(img_bytes, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

def extract_eye(base64_img, save_path=None):
    img = decode_image(base64_img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
    if len(eyes) == 0:
        return None
    x, y, w, h = eyes[0]
    eye = gray[y:y+h, x:x+w]
    resized = cv2.resize(eye, (64, 64))
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        cv2.imwrite(save_path, resized)
    _, buffer = cv2.imencode('.png', resized)
    return base64.b64encode(buffer).decode("utf-8")

# ------------------ Registration ------------------

def register_user(data):
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"success": False, "message": "Missing fields"}), 400
    if users_collection.find_one({"email": email}):
        return jsonify({"success": False, "message": "User already exists"}), 409
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user_id = str(ObjectId())
    users_collection.insert_one({
        "user_id": user_id,
        "email": email,
        "password": hashed_pw.decode("utf-8"),
        "iris_image": None
    })
    return jsonify({"success": True, "message": "User registered"}), 201

# ------------------ OTP ------------------

def send_otp(data):
    email = data.get("email")
    if not email:
        return jsonify({"success": False, "message": "Email required"}), 400
    if not users_collection.find_one({"email": email}):
        return jsonify({"success": False, "message": "User not found"}), 404
    otp = generate_otp()
    otp_store[email] = otp
    print(f"DEBUG OTP: {otp} for {email}")
    if send_otp_email(email, otp):
        return jsonify({"success": True, "message": "OTP sent"}), 200
    else:
        return jsonify({"success": False, "message": "Failed to send OTP"}), 500

def verify_otp(data):
    email = data.get("email")
    otp_entered = str(data.get("otp"))
    if not email or not otp_entered:
        return jsonify({"success": False, "message": "Missing email or OTP"}), 400
    correct_otp = get_otp_for(email)
    if not correct_otp:
        return jsonify({"success": False, "message": "No OTP found. Try again."}), 404
    if otp_entered == correct_otp:
        reset_attempts(email)
        otp_store.pop(email, None)
        return jsonify({"success": True, "message": "OTP verified"}), 200
    else:
        attempts = increment_attempt(email)
        if attempts >= 3:
            return jsonify({"success": False, "message": "3 wrong attempts. Blocked."}), 403
        return jsonify({"success": False, "message": f"Wrong OTP ({attempts}/3)"}), 401

# ------------------ Password ------------------

def verify_password(data):
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"success": False, "message": "Missing email or password"}), 400
    user = users_collection.find_one({"email": email})
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    if bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        return jsonify({"success": True, "message": "Password correct"}), 200
    return jsonify({"success": False, "message": "Incorrect password"}), 401

# ------------------ Iris Upload ------------------

def upload_iris(data):
    email = data.get("email")
    base64_img = data.get("image")
    if not email or not base64_img:
        return jsonify({"success": False, "message": "Missing data"}), 400
    eye_img_b64 = extract_eye(base64_img, save_path=f"debug_iris/registered_{email}.png")
    if not eye_img_b64:
        return jsonify({"success": False, "message": "No eye detected"}), 400
    users_collection.update_one(
        {"email": email},
        {"$set": {"iris_image": eye_img_b64}}
    )
    return jsonify({"success": True, "message": "Iris uploaded"}), 200

# ------------------ Iris Verification ------------------

def verify_iris(data):
    email = data.get("email")
    base64_img = data.get("image")
    if not email or not base64_img:
        return jsonify({"success": False, "message": "Missing data"}), 400
    user = users_collection.find_one({"email": email})
    if not user or not user.get("iris_image"):
        return jsonify({"success": False, "message": "No stored iris"}), 404

    def decode_gray(b64_img):
        img_bytes = base64.b64decode(b64_img.split(",")[1])
        return cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_GRAYSCALE)

    try:
        stored_img = decode_gray("data:image/png;base64," + user["iris_image"])
        live_b64 = extract_eye(base64_img, save_path=f"debug_iris/live_{email}.png")
        if not live_b64:
            return jsonify({"success": False, "message": "No eye detected"}), 400
        test_img = decode_gray("data:image/png;base64," + live_b64)

        if stored_img.shape != test_img.shape:
            test_img = cv2.resize(test_img, (stored_img.shape[1], stored_img.shape[0]))

        diff = np.abs(stored_img.astype(np.int32) - test_img.astype(np.int32))
        score = np.mean(diff)

        if score < 10:  # Threshold – adjust based on environment
            return jsonify({"success": True, "message": "Iris matched"}), 200
        else:
            return jsonify({"success": False, "message": "Iris did not match"}), 403

    except Exception as e:
        print("❌ Verification error:", e)
        return jsonify({"success": False, "message": "Verification failed"}), 500
