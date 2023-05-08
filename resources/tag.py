from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from db import db
from schemas import TagSchema, TagAndItemSchema
from models import TagModel, StoreModel, ItemModel

tag_api = Blueprint("Tags", "tags", description="Operates on tags")


@tag_api.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @jwt_required()
    @tag_api.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        return store.tags.all()

    @jwt_required()
    @tag_api.arguments(TagSchema)
    @tag_api.response(201, TagSchema)
    def post(self, tag_data, store_id):
        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()

        except SQLAlchemyError as e:
            abort(
                500,
                message=f"An error occured while creating a tag for the store '{store_id}', error:\n{str(e)}",
            )

        return tag


@tag_api.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @jwt_required()
    @tag_api.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        return tag

    @jwt_required(fresh=True)
    @tag_api.response(
        202,
        description="Deletes a tag if no items is linked with it.",
        example={"message": "Tag deleted."},
    )
    @tag_api.alt_response(404, description="Tag not found")
    @tag_api.alt_response(
        400,
        description="Returned if the tag is linked with items, the tag is not deleted in this case.",
    )
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()

            return {"message": "Tag deleted."}
        else:
            abort(
                400,
                description="Failed to delete tag, please ensure the tag is not linked to any item, then try again.",
            )

        return tag


@tag_api.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @jwt_required()
    @tag_api.response(201, TagSchema)
    def post(self, tag_id, item_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message="An error occured while linking tag: '{tag}' to item: '{item}', error: \n{e}",
            )

        return tag


@tag_api.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @jwt_required(fresh=True)
    @tag_api.response(200, TagAndItemSchema)
    def delete(self, tag_id, item_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message="An error occured while unlinking tag: '{tag}' from item: '{item}', error: \n{e}",
            )

        return {"message": "Item unlinked successfully", "item": item, "tag": tag}
