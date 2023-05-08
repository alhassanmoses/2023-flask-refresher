from typing import Any
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

item_api = Blueprint("items", __name__, description="Operations on items.")


@item_api.route("/item/<int:item_id>")
class Store(MethodView):
    @jwt_required()
    @item_api.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)

        return item

    @jwt_required(fresh=True)
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        item = ItemModel.query.get(item_id)
        db.session.delete(item)
        db.session.commit()

        return {"message": "Item deleted."}

    @jwt_required()
    @item_api.arguments(ItemUpdateSchema)
    @item_api.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)

        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item
        raise NotImplementedError("Updating an item is not implemented.")


@item_api.route("/item")
class Store(MethodView):
    @jwt_required()
    @item_api.arguments(ItemSchema)
    @item_api.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while creating the item model in db.")

        return item

    @jwt_required()
    @item_api.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
