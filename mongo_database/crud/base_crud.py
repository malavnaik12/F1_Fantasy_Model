from models.base_model import Item
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

def create_item(main_collection: Collection, item: Item):
    item.version = 1
    main_collection.insert_one(item.model_dump())
    return item

def read_item(main_collection: Collection, name: str):
    result = main_collection.find_one({"name": name})
    return result

def update_item(main_collection: Collection, cache_collection: Collection, name: str, item: Item):
    find_item = main_collection.find_one({"name": name})
    if find_item:
        try:
            cache_collection.insert_one(find_item)
        except DuplicateKeyError:
            cache_collection.update_one({"name": name}, {"$set": find_item}, upsert=True)
        item.version = find_item['version']+1
    else:
        item.version = 1
    result = main_collection.update_one({"name": name}, {"$set": item.model_dump()}, upsert=True)

    return result

def delete_item(main_collection: Collection,name: str):
    result = main_collection.delete_one({"name": name})
    return None