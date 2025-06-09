from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.iris_routes import iris_bp
from routes.resource_routes import resource_bp
from routes.honeypot_routes import honeypot_bp
from db import db
import os

app = Flask(__name__)

# ✅ Enable CORS for local development and deployed frontend
CORS(app, supports_credentials=True, origins=[
    "http://localhost:3000",
    "https://secureiris-mfa.onrender.com"
])

# ✅ Register routes (blueprints)
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(iris_bp, url_prefix="/api/iris")
app.register_blueprint(resource_bp, url_prefix="/api/resource")
app.register_blueprint(honeypot_bp, url_prefix="/api/honeypot")

# ✅ Test DB connection
@app.route("/test_db")
def test_db():
    try:
        user = db.users.find_one()
        return {"message": "MongoDB Atlas connected!", "sample_user": str(user)}
    except Exception as e:
        return {"error": str(e)}

# ✅ Run on PORT 5050 locally or on Render's assigned port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port)
