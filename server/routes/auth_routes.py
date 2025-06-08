from flask import Blueprint, request, jsonify
from controllers.auth_controller import (
    register_user, send_otp, verify_otp, verify_password
)
from models.user_model import users_collection  # 🔁 Needed for unblock route

# Create blueprint for authentication
auth_bp = Blueprint("auth", __name__)

# Register route
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    return register_user(data)

# Send OTP
@auth_bp.route("/send-otp", methods=["POST"])
def send_otp_route():
    data = request.get_json()
    return send_otp(data)

# Verify OTP
@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp_route():
    data = request.get_json()
    return verify_otp(data)

# Verify password
@auth_bp.route("/verify-password", methods=["POST"])
def verify_password_route():
    data = request.get_json()
    return verify_password(data)

# 🔐 Get Client IP (for fake page logging)
@auth_bp.route("/get-ip", methods=["GET"])
def get_ip():
    ip = request.remote_addr
    return jsonify({"ip": ip})

# 🔓 Unblock User (dev use only)
@auth_bp.route("/unblock", methods=["POST"])
def unblock_user():
    email = request.json.get("email")
    if not email:
        return jsonify({"success": False, "message": "Email required"}), 400

    result = users_collection.update_one(
        {"email": email},
        {"$set": {"blocked": False, "otp_attempts": 0}}
    )

    if result.modified_count == 1:
        return jsonify({"success": True, "message": "User unblocked"}), 200
    else:
        return jsonify({"success": False, "message": "User not found or not updated"}), 404
