import fastapi
from models.drivers_model import Drivers
from drivers_collection import get_col_Drivers, get_col_Drivers_cache
from crud import drivers_crud

router = fastapi.APIRouter()

@router.post("/drivers/", response_model=Drivers)
def create_item(item: Drivers, collection=fastapi.Depends(get_col_Drivers)):
    return drivers_crud.create_item(collection,item)

@router.get("/drivers/", response_model=Drivers)
def read_item(name: str = None, team: str = None, race: str = None, collection=fastapi.Depends(get_col_Drivers)):
    item = drivers_crud.read_item(collection, name, team, race)
    if item is None:
        raise fastapi.HTTPException(status_code=404, detail="Read Drivers: Driver not found")
    return item

@router.put("/drivers/", response_model=Drivers)
def update_item(name: str = None, team: str = None, race: str = None, item: Drivers = None, main_collection=fastapi.Depends(get_col_Drivers), cache_collection=fastapi.Depends(get_col_Drivers_cache)):
    result = drivers_crud.update_item(main_collection,cache_collection,name,team,item,race)
    if result.matched_count == 0:
        raise fastapi.HTTPException(status_code=404, detail="Update Drivers: Driver not found")
    return item

@router.delete("/drivers/", status_code=200)
def delete_item(name: str = None, collection=fastapi.Depends(get_col_Drivers)):
    result = drivers_crud.delete_item(collection,name)
    if result.deleted_count == 0:
        raise fastapi.HTTPException(status_code=404, detail="Delete Drivers: Driver not found")
    return None