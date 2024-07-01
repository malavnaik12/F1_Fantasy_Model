import fastapi
from models.base_model import Item
from base_database import get_col_Constructors
from crud.base_crud import create_item, read_item, update_item, delete_item

router = fastapi.APIRouter()

@router.post("/constructors", response_model=Item)
def create_item(item: Item, collection=fastapi.Depends(get_col_Constructors)):
    # col_constructors.insert_one(item.model_dump())
    return create_item(collection,item)

@router.get("/constructors/{name}", response_model=Item)
def read_item(name: str, collection=fastapi.Depends(get_col_Constructors)):
    item = read_item(collection, name)
    if item is None:
        raise fastapi.HTTPException(status_code=404, detail="Read Item: Item not found")
    return item

@router.put("/constructors/{name}", response_model=Item)
def update_item(name: str, item: Item, collection=fastapi.Depends(get_col_Constructors)):
    result = update_item(collection,name,item)
    if result.matched_count == 0:
        raise fastapi.HTTPException(status_code=404, detail="Update Item: Item not found")
    return item

@router.delete("/constructors/{name}", status_code=204)
def delete_item(name: str, collection=fastapi.Depends(get_col_Constructors)):
    result = delete_item(collection,name)
    if result.deleted_count == 0:
        raise fastapi.HTTPException(status_code=404, detail="Delete Item: Item not found")
    return None