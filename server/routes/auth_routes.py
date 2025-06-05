# server/routes/auth_routes.py — Handles user registration and OTP operations
from flask import Blueprint, request, jsonify
from controllers.auth_controller import register_user, send_otp, verify_otp, upload_iris

# Create blueprint for authentication
auth_bp = Blueprint("auth", __name__)

# Registration route
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    return register_user(data)

# Send OTP to email
@auth_bp.route("/send-otp", methods=["POST"])
def send_otp_route():
    data = request.get_json()
    return send_otp(data)

# Verify OTP
@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp_route():
    data = request.get_json()
    return verify_otp(data)

# Upload iris image (during registration step)
@auth_bp.route("/iris-upload", methods=["POST"])
def iris_upload_route():
    data = request.get_json()
    return upload_iris(data)
