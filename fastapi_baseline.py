import pymongo
import fastapi
from pydantic import BaseModel
from typing import List

app = fastapi.FastAPI()
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["constructors"]

# Define a Pydantic model
class Item(BaseModel):
    name: str
    fp: List[float]
    quali_hist: List[float]
    race_hist: List[float]
    price: List[float]

@app.post("/items", response_model=Item)
def create_item(item: Item):
    mycol.insert_one(item.model_dump())
    return item

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)