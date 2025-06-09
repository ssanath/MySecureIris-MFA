from flask import Blueprint, request, jsonify
from datetime import datetime
import pytz
from db import db
from user_agents import parse  # 🧠 External parser for better detection

honeypot_bp = Blueprint("honeypot", __name__)
honeypot_logs = db["honeypot_logs"]

@honeypot_bp.route("/log", methods=["POST"])
def log_honeypot_action():
    data = request.get_json()
    ua_string = request.headers.get("User-Agent")
    parsed_ua = parse(ua_string)

    # ✅ Get current IST time in plain string format
    ist = pytz.timezone("Asia/Kolkata")
    timestamp_ist_str = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")  # e.g., "2025-06-09 15:30:12"

    log_entry = {
        "ip": request.remote_addr,
        "route": data.get("route", ""),
        "action": data.get("action", ""),
        "userAgent": ua_string,
        "timestamp": timestamp_ist_str,
        "email": data.get("email", ""),
        "browser": parsed_ua.browser.family,
        "platform": parsed_ua.os.family,
        "deviceType": parsed_ua.device.family,
        "language": request.headers.get("Accept-Language"),
        "screenSize": data.get("screenSize", ""),
        "fakePayload": data.get("payload", {})
    }

    honeypot_logs.insert_one(log_entry)
    return jsonify({"success": True, "message": "Logged honeypot action"}), 201
