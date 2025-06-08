from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.iris_routes import iris_bp
from routes.resource_routes import resource_bp
from routes.honeypot_routes import honeypot_bp
from db import db
import os  # ✅ Required to read PORT

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(iris_bp, url_prefix="/api/iris")
app.register_blueprint(resource_bp, url_prefix="/api/resource")
app.register_blueprint(honeypot_bp, url_prefix="/api/honeypot")

@app.route("/test_db")
def test_db():
    try:
        user = db.users.find_one()
        return {"message": "MongoDB Atlas connected!", "sample_user": str(user)}
    except Exception as e:
        return {"error": str(e)}

# ✅ CORRECT entrypoint for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
