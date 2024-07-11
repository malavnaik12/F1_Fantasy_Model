import fastapi
from mongo_database.models.constructors_model import Constructors
from mongo_database.collections.constructors_collection import get_col_Constructors, get_col_Constructors_cache
from mongo_database.crud import constructors_crud

router = fastapi.APIRouter()

@router.post("/constructors", response_model=Constructors)
def create_item(item: Constructors, collection=fastapi.Depends(get_col_Constructors)):
    return constructors_crud.create_item(collection,item)

@router.get("/constructors/", response_model=Constructors)
def read_item(name: str = None, race: str = None, collection=fastapi.Depends(get_col_Constructors)):
    item = constructors_crud.read_item(collection, name, race)
    if item is None:
        raise fastapi.HTTPException(status_code=404, detail="Read Constructors: Constructors not found")
    return item

@router.put("/constructors/", response_model=Constructors)
def update_item(name: str = None, race: str = None, item: Constructors = None, main_collection=fastapi.Depends(get_col_Constructors), cache_collection=fastapi.Depends(get_col_Constructors_cache)):
    result = constructors_crud.update_item(main_collection,cache_collection,name,item,race)
    if result.matched_count == 0:
        raise fastapi.HTTPException(status_code=404, detail="Update Constructors: Constructors not found")
    return item

@router.delete("/constructors/", status_code=204)
def delete_item(name: str = None, collection=fastapi.Depends(get_col_Constructors)):
    result = constructors_crud.delete_item(collection,name)
    if result.deleted_count == 0:
        raise fastapi.HTTPException(status_code=404, detail="Delete Constructors: Constructors not found")
    return None