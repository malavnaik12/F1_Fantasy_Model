from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel
from team_parse import getTeams, getDrivers
from weekend_parse import gp_parse,sessions_parse
from database_operations import InsertData

# weekend_info = WeekendParser()
insert2db = InsertData()
router = APIRouter()
class Item(BaseModel):
    year: Optional[int] = None
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
    gp_locs = gp_parse()
    return {'entity':gp_locs}

@router.post('/sessions/')
async def send_session_types(item: Item):
    locs = sessions_parse(item.raceLoc)
    return {'entity':locs}

@router.get('/constructors/')
async def send_constructors():
    return {'entity':getTeams()}

@router.post('/drivers/')
async def send_drivers(item: Item):
    inputs = {}
    for entity in list(item):
        inputs[entity[0]] = entity[1]
        if item.constructor in getTeams():
            drivers = getDrivers(item.constructor)
            inputs['driver1'] = drivers[0]
            inputs['driver2'] = drivers[1]
    return {"status": "success", "entity": inputs}

@router.post('/session_info/')
async def get_session_info(item: Item):
    inputs = {}
    for entity in list(item):
        inputs[entity[0]] = entity[1]
    try:
        response = insert2db.get_session(inputs)
    except ValueError:
        response = False
        print("No data found:",response)
    return {"status":"success","entity":response}

@router.post('/submit/')
async def send_info_to_DBs(item: Item):
    inputs = {}
    for entity in list(item):
        inputs[entity[0]] = entity[1]
    insert2db.init_race_weekend(race_loc=inputs['raceLoc'])
    insert2db.post_race(item_dict=inputs)
    return {"status": "success", "entity": "1) Need to populate race_results.json with all race results. 2) May need to rethink driver inputs. It's kind of cumbersome to go through each constructor manually."}
            # 3) Also add some timed effect that slowly changes positions of driver positions if the inputs change.  4) Update readme how to merge to prod branch and push to prod as well."}