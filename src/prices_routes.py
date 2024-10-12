from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel
from team_parse import getTeams, getDrivers
from weekend_parse import get_gp_info,gp_parse,sessions_parse
from database_operations import InsertData

insert2db = InsertData()
prices_router = APIRouter()
class Item(BaseModel):
    year: Optional[int] = None
    raceLoc: Optional[str] = None
    session: Optional[str] = None
    drivers: Optional[list] = None
    prices: Optional[list] = None
    # constructor: Optional[str] = None
    # driver1: Optional[str] = None
    # driver2: Optional[str] = None
    # driver1_pos: Optional[int] = None
    # driver2_pos: Optional[int] = None
    # data_override: Optional[bool] = None
    # substitute_driver: Optional[bool] = None
    # substitute_driver_name: Optional[str] = None
    # substitute_driver_pos: Optional[int] = None

@prices_router.get('/gp_locs/')
async def send_gp_dropdown():
    gp_locs = gp_parse(get_gp_info())
    return {'entity':gp_locs}

@prices_router.post('/sessions/')
async def send_session_types(item: Item):
    return {'entity':sessions_parse(item.raceLoc)}

@prices_router.post('/session_info/')
async def get_session_info(item: Item):
    inputs = {}
    for entity in list(item):
        inputs[entity[0]] = entity[1]
    try:
        response = insert2db.get_session(inputs)
    except ValueError:
        response = False
        raise(f"No data found for {item}")
    return {"status":"success","entity":response}

@prices_router.post('/prices_submit/')
async def send_info_to_DBs(item: Item):
    inputs = {}
    for entity in list(item):
        inputs[entity[0]] = entity[1]
    # try:
    #     response = insert2db.get_session(inputs)
    # except ValueError:
    #     response = False
    #     raise(f"No data found for {item}")
    print(inputs)
    return {"status":"success","entity":inputs}