from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.iris_routes import iris_bp

app = Flask(__name__)

# Enable CORS so React frontend (localhost:3000) can access the Flask API (localhost:5050)
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

# Register authentication routes with prefix /api/auth
app.register_blueprint(auth_bp, url_prefix="/api/auth")

# Register iris-related routes with prefix /api/iris
app.register_blueprint(iris_bp, url_prefix="/api/iris")

if __name__ == "__main__":
    app.run(debug=True, port=5050)
