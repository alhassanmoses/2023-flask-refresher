import uuid
from typing import Any
from flask import Flask, request
from db import stores, items
from flask_smorest import abort

app = Flask(__name__)


@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.get("/store/<string:store_id>")
def get_store(store_id):
    store = stores.get(store_id, False)
    if store:
        return store
    abort(404, message="Store not found.")


@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}


@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted."}
    except KeyError:
        abort(404, message="Store not found.")


@app.post("/item")
def create_item():
    item_data = request.get_json()
    if (
        ("price" not in item_data)
        or ("store_id" not in item_data)
        or ("name" not in item_data)
    ):
        abort(
            400,
            message="Bad request, please ensure 'price', 'store_id' and 'name' are all included in the JSON payload.",
        )

    for item in items.values():
        if (item_data["name"] == item["name"]) and (
            item_data["store_id"] == item["store_id"]
        ):
            abort(400, message="Item already exists.")
    if item_data["store_id"] not in stores:
        abort(404, message="Store not found.")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item, 201


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found.")


@app.get("/item")
def get_items():
    return {"items": list(items.values())}


@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(
            400,
            message="Bad request. Please ensure a 'price' and 'name' are both provided in the request payload.",
        )
    try:
        item: dict[str, Any] = items[item_id]
        # Dictionary update operator ('|='), first takes in item, then updates/overrides it with data from item_data
        item |= item_data

        return item
    except KeyError:
        abort(404, message="Item not found.")


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        abort(404, message="Item not found.")
