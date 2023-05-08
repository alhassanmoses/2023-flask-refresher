import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from db import db
import models
from blocklist import BLOCKLIST

from resources.item import item_api as ItemBlueprint
from resources.store import store_api as StoreBlueprint
from resources.tag import tag_api as TagBlueprint
from resources.user import user_api as UserBlueprint


def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "SRORES REST APIs"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"  # Swagger URL: http://localhost:5005/swagger-ui
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.environ.get("APP_SECRET")
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.needs_fresh_token_loader
    def non_fresh_token_callback(jwt_header, jwt_payload):
        return jsonify(
            {
                "description": "Non-fresh token provided.",
                "error": "fresh_token_required",
            }
        )

    @jwt.revoked_token_loader
    def revoke_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token being used has been revoked.",
                    "error": "token_revoked",
                }
            ),
            401,
        )

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # Extract the Identity
        # Query the db for the user
        # Verify whether the user is an admin or not and add the result as a claim
        # return {"is_admin": True if user.id == awesome else False}
        pass

    @jwt.expired_token_loader
    def exppired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def exppired_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "Invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def exppired_token_callback(error):
        return (
            jsonify(
                {
                    "description": "The request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
