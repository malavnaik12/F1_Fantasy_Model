from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel
from team_parse import getTeams, getDrivers
from weekend_parse import get_gp_info,gp_parse,sessions_parse
from database_operations import InsertData

db_ops = InsertData()
router = APIRouter()
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

@router.get('/gp_locs/')
async def send_gp_dropdown():
    gp_locs = gp_parse(get_gp_info())
    return {'entity':gp_locs}

@router.post('/sessions/')
async def send_session_types(item: Item):
    return {'entity':sessions_parse(item.raceLoc)}

@router.post('/session_info/')
async def get_session_info(item: Item):
    inputs = {}
    for entity in list(item):
        inputs[entity[0]] = entity[1]
    try:
        response = {}
        response['driver_positions'] = db_ops.get_session(inputs)
        # constructors_list = db_ops.get_session_constructors(inputs,response['driver_positions'])
        driver_prices_dict = db_ops.get_driver_prices(inputs)
        response['constructor_prices'] = db_ops.get_constructor_prices(inputs)
        if len(driver_prices_dict) == 0:
            response['driver_prices'] = []
        else:
            response['driver_prices'] = [driver_prices_dict[f"{driver}"] for driver in response['driver_positions']]
    except ValueError:
        response = False
        raise(f"No data found for {item}")
    return {"status":"success","entity":response}

# @router.post('/prices_pull')
# async def get_info_from_db(item: Item):
#     inputs = {}
#     for entity in list(item):
#         inputs[entity[0]] = entity[1]
#     prices_dict = db_ops.get_prices(inputs) # This return a dictionary of prices
#     positions = db_ops.get_session(inputs)
#     print(positions)

@router.post('/prices_submit/')
async def send_info_to_DBs(item: Item):
    inputs = {}
    response = {}
    for entity in list(item):
        inputs[entity[0]] = entity[1]
    print(inputs)
    input()
    response = db_ops.post_driver_prices(inputs)
    db_ops.post_constructor_prices(inputs)
    # try:
    #     response = db_ops.get_session(inputs)
    # except ValueError:
    #     response = False
    #     raise(f"No data found for {item}")
    # print(response)
    response = "success"
    return {"status":"success","entity":response}