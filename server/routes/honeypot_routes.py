from flask import Blueprint, request, jsonify
from datetime import datetime
from db import db
from user_agents import parse  # 🧠 External parser for better detection

honeypot_bp = Blueprint("honeypot", __name__)
honeypot_logs = db["honeypot_logs"]

@honeypot_bp.route("/log", methods=["POST"])
def log_honeypot_action():
    data = request.get_json()
    ua_string = request.headers.get("User-Agent")
    parsed_ua = parse(ua_string)

    log_entry = {
        "ip": request.remote_addr,
        "route": data.get("route", ""),
        "action": data.get("action", ""),
        "userAgent": ua_string,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "email": data.get("email", ""),
        "browser": parsed_ua.browser.family,       # ✅ e.g., Chrome
        "platform": parsed_ua.os.family,           # ✅ e.g., macOS
        "deviceType": parsed_ua.device.family,     # ✅ e.g., Mac, iPhone, etc.
        "language": request.headers.get("Accept-Language"),
        "screenSize": data.get("screenSize", ""),  # Optional: sent from frontend
        "fakePayload": data.get("payload", {})     # Optional: any fake data passed
    }

    honeypot_logs.insert_one(log_entry)
    return jsonify({"success": True, "message": "Logged honeypot action"}), 201
