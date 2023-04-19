import uuid

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from schemas import StoreSchema
from models import StoreModel

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

store_api = Blueprint("stores", __name__, description="Operations on stores.")


@store_api.route("/store/<string:store_id>")
class Store(MethodView):
    @store_api.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()

        return {"message": "Store deleted."}


@store_api.route("/store")
class Store(MethodView):
    @store_api.arguments(StoreSchema)
    @store_api.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Sorry, a store with the given name already exist.")
        except SQLAlchemyError:
            abort(500, message="An error occured while creating the store model in db.")

        return store

    @store_api.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
