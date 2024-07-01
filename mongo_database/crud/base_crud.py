from models.base_model import Item
from pymongo.collection import Collection

def create_item(collection: Collection, item: Item):
    collection.insert_one(item.model_dump())
    return item

def read_item(collection: Collection, name: str):
    result = collection.find_one({"name": name})
    # if item is None:
    #     raise fastapi.HTTPException(status_code=404, detail="Read Item: Item not found")
    return result

def update_item(collection: Collection, name: str, item: Item):
    result = collection.update_one({"name": name}, {"$set": item.model_dump()})
    # if result.matched_count == 0:
    #     raise fastapi.HTTPException(status_code=404, detail="Update Item: Item not found")
    return result

def delete_item(collection: Collection,name: str):
    result = collection.delete_one({"name": name})
    # if result.deleted_count == 0:
    #     raise fastapi.HTTPException(status_code=404, detail="Delete Item: Item not found")
    return None