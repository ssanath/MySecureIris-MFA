from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.iris_routes import iris_bp
from routes.resource_routes import resource_bp  # moved here
from db import db

app = Flask(__name__)  # ✅ this must come first

# Enable CORS
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(iris_bp, url_prefix="/api/iris")
app.register_blueprint(resource_bp, url_prefix="/api/resource")  # ✅ move here

@app.route("/test_db")
def test_db():
    try:
        user = db.users.find_one()
        return {"message": "MongoDB Atlas connected!", "sample_user": str(user)}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    app.run(debug=True, port=5050)
