import pymongo
import fastapi
from typing import List
from mongo_database.models.base_model import Item

app = fastapi.FastAPI(title="F1 Fantasy App Database")
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
col_constructors = mydb["constructors"]
col_drivers = mydb["drivers"]

# # Define a Pydantic model
# class Item(BaseModel):
#     name: str
#     fp: List[float]
#     quali_hist: List[float]
#     race_hist: List[float]
#     price: List[float]

@app.post("/constructors", response_model=Item)
def create_item(item: Item):
    col_constructors.insert_one(item.model_dump())
    # col_drivers.insert_one(item.model_dump())
    return item

@app.get("/constructors", response_model=List[Item])
def read_items():
    items = list(col_constructors.find({}, {"_id": 0}))
    return items

@app.get("/constructors/{name}", response_model=Item)
def read_item(name: str):
    item = col_constructors.find_one({"name": name})
    if item is None:
        raise fastapi.HTTPException(status_code=404, detail="Read Item: Item not found")
    return item

@app.put("/constructors/{name}", response_model=Item)
def update_item(name: str, item: Item):
    result = col_constructors.update_one({"name": name}, {"$set": item.model_dump()})
    if result.matched_count == 0:
        raise fastapi.HTTPException(status_code=404, detail="Update Item: Item not found")
    return item

@app.delete("/constructors/{name}", status_code=204)
def delete_item(name: str):
    result = col_constructors.delete_one({"name": name})
    if result.deleted_count == 0:
        raise fastapi.HTTPException(status_code=404, detail="Delete Item: Item not found")
    return None

if __name__ == '__main__':
    import uvicorn
    # app.include_router(prefix='/docs')
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)