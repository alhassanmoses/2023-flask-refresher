from marshmallow import Schema, fields


# ================== Plain Schemas ==================
# Item Schemas
class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


# Store Schemas
class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


# Tag Schemas
class PlainTagSchema(Schema):
    id = fields.Int(dumps_only=True)
    name = fields.Str(required=True)


# ================== Schemas ==================
# Item Schemas
class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainItemSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema), dumps_only=True)


# Store Schemas
class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainStoreSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


# Tag Schemas
class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema), dumps_only=True)


# ItemsTag Schemas
class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)
