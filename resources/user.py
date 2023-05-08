from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt,
    create_refresh_token,
    get_jwt_identity,
)
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256

from db import db
from blocklist import BLOCKLIST
from schemas import UserSchema
from models import UserModel

user_api = Blueprint("Users", "users", description="Operates on users")


@user_api.route("/register")
class UserRegistration(MethodView):
    @user_api.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )

        try:
            db.session.add(user)
            db.session.commit()

            return {"message": "User created successfully"}, 201
        except SQLAlchemyError as e:
            abort(
                409,
                message=f"An error occured while creating a user object, error: \n{e}",
            )


@user_api.route("/user/<int:user_id>")
class UserRegistration(MethodView):
    @user_api.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        db.session.delete(user)
        db.session.commit()

        return {"message": "User delete."}, 200


@user_api.route("/login")
class UserLogin(MethodView):
    @user_api.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)

            return {"access_token": access_token, "refresh_token": refresh_token}

        abort(401, message="Invalid credentials provided.")


@user_api.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)

        return {"access_token": new_token}


@user_api.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self, user_data):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)

        return {"message": "Logged out successfully."}
