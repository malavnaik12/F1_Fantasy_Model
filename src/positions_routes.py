from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel
from team_parse import getTeams, getDrivers
from weekend_parse import WeekendParser
from database_operations import InsertData

weekend_info = WeekendParser()
insert2db = InsertData()
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
def send_gp_dropdown():
    return {'entity':weekend_info.gp_parse()}

@router.post('/sessions/')
def send_session_types(item: Item):
    return {'entity':weekend_info.sessions_parse(item.raceLoc)}

@router.get('/constructors/')
def send_constructors():
    return {'entity':getTeams()}

@router.post('/drivers/')
def send_drivers(item: Item):
    inputs = {}
    for entity in list(item):
        inputs[entity[0]] = entity[1]
        if item.constructor in getTeams():
            drivers = getDrivers(item.constructor)
            inputs['driver1'] = drivers[0]
            inputs['driver2'] = drivers[1]
    return {"status": "success", "entity": inputs}

@router.post('/session_info/')
def get_session_info(item: Item):
    inputs = {}
    for entity in list(item):
        inputs[entity[0]] = entity[1]
    response = insert2db.get_session(inputs)
    return {"status":"success","entity":response}

@router.post('/submit/')
def send_info_to_DBs(item: Item):
    inputs = {}
    for entity in list(item):
        inputs[entity[0]] = entity[1]
    insert2db.init_race_weekend(race_loc=inputs['raceLoc'])
    insert2db.post_race(item_dict=inputs)
    return {"status": "success", "entity": "1) Need to build out the backend insertion code, where there is a reponse after 'submit' operation. 2) Update readme how to merge to prod branch and push to prod as well."}