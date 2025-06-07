# otp_util.py – OTP generation, email sending, attempt tracking

import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Stores OTPs temporarily: { email: "123456" }
otp_store = {}

# Stores OTP verification attempts: { email: 1, 2, 3 }
otp_attempts = {}

# Generate a random 6-digit OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Send OTP to user via email
def send_otp_email(receiver_email, otp):
    sender_email = "pjyotsna2603@gmail.com"      # ✅ your Gmail
    sender_password = "iwiwkqeprwfmxdav"          # ✅ your Gmail App Password

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
        print(f"Email send error: {e}")
        return False

# Get the stored OTP for a given email
def get_otp_for(email):
    return otp_store.get(email)

# Increment and return OTP attempt count
def increment_attempt(email):
    otp_attempts[email] = otp_attempts.get(email, 0) + 1
    return otp_attempts[email]

# Reset OTP attempt count after success
def reset_attempts(email):
    otp_attempts.pop(email, None)

# Clear OTP from memory after success
def clear_otp(email):
    otp_store.pop(email, None)
