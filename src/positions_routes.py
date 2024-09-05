from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel
from team_parse import getTeams, getDrivers
from weekend_parse import WeekendParser

weekend_info = WeekendParser()
router = APIRouter()
class Item(BaseModel):
    raceLoc: Optional[str] = None
    session: Optional[str] = None
    constructor: Optional[str] = None
    driver1: Optional[str] = None
    driver2: Optional[str] = None
    driver1_pos: Optional[int] = None
    driver2_pos: Optional[int] = None
    data_override: Optional[bool] = None
    substitute_driver: Optional[bool] = None
    substitute_driver_name: Optional[str] = None
    substitute_driver_pos: Optional[int] = None

@router.get('/gp_locs/')
async def send_gp_dropdown():
    return {'entity':weekend_info.gp_parse()}

@router.post('/sessions/')
async def send_session_types(item: Item):
    print(item)
    return {'entity':weekend_info.sessions_parse(item.raceLoc)}

@router.get('/constructors/')
async def send_constructors():
    return {'entity':getTeams()}

@router.post('/submit/')
async def post_gp_dropdown(item: Item):
    inputs = {}
    print(item)
    for entity in list(item):
        inputs[entity[0]] = entity[1]
        if item.constructor in getTeams():
            drivers = getDrivers(item.constructor)
            inputs['driver1'] = drivers[0]
            inputs['driver2'] = drivers[1]
    print(f"{inputs}")
    return {"status": "success", "entity": inputs}