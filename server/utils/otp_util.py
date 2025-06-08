import smtplib
import random
import os
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()
sender_email = os.getenv("EMAIL_USER")
sender_password = os.getenv("EMAIL_PASS")

otp_store = {}
otp_attempts = {}

# Generate a random 6-digit OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Send OTP to user via email
def send_otp_email(receiver_email, otp):
    subject = "Your OTP Code"
    body = f"Your OTP code is: {otp}"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"❌ Email send error: {e}")
        return False

# Send suspicious activity alert to yourself
def send_alert_email(email, ip):
    subject = "🚨 Suspicious Activity Detected"
    body = f"""
    Suspicious login attempt detected!

    Email: {email}
    IP Address: {ip}
    Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    This user has been blocked after 3 failed OTP attempts.
    """

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = sender_email  # Send alert to yourself
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, sender_email, msg.as_string())
        server.quit()
        print("🚨 Alert email sent!")
        return True
    except Exception as e:
        print("❌ Failed to send alert email:", e)
        return False

# OTP store helpers
def get_otp_for(email):
    return otp_store.get(email)

def increment_attempt(email):
    otp_attempts[email] = otp_attempts.get(email, 0) + 1
    return otp_attempts[email]

def reset_attempts(email):
    otp_attempts.pop(email, None)

def clear_otp(email):
    otp_store.pop(email, None)
