import os
import sys
from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# When started with `python app.py`, expose this module as `app` so
# imports like `from app import mongo` resolve to the initialized instance.
sys.modules.setdefault("app", sys.modules[__name__])

mongo = PyMongo()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    load_dotenv()
    app = Flask(__name__)

    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "change-me")

    CORS(app)
    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from routes.auth_routes import auth_bp
    from routes.user_routes import user_bp
    from routes.admin_routes import admin_bp
    from routes.verifier_routes import verifier_bp
    from routes.claim_routes import claim_bp

    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(verifier_bp, url_prefix="/api/verifier")
    app.register_blueprint(claim_bp, url_prefix="/api/claims")

    @app.get("/api/health")
    def health_check():
        return {"status": "ok"}, 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
