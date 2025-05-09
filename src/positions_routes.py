from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel
from team_parse import getTeams, getDrivers
from weekend_parse import get_gp_info, gp_parse, sessions_parse
from database_operations import InsertData
from rr_to_DBmain import rr_to_DBmain

# weekend_info = WeekendParser()
db_ops = InsertData()
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


@router.get("/gp_locs/")
def send_gp_dropdown():
    gp_locs = gp_parse(get_gp_info())
    return {"entity": gp_locs}


@router.post("/sessions/")
def send_session_types(item: Item):
    locs = sessions_parse(item.raceLoc)
    return {"entity": locs}


@router.get("/constructors/")
def send_constructors():
    return {"entity": getTeams()}


@router.post("/drivers/")
def send_drivers(item: Item):
    inputs = {}
    for entity in list(item):
        inputs[entity[0]] = entity[1]
        if item.constructor in getTeams():
            drivers = getDrivers(item.constructor)
            inputs["driver1"] = drivers[0]
            inputs["driver2"] = drivers[1]
    return {"status": "success", "entity": inputs}


@router.post("/session_info/")
def get_session_info(item: Item):
    inputs = {}
    response = {}
    for entity in list(item):
        inputs[entity[0]] = entity[1]
    db_ops.__init__(inputs["year"])
    try:
        response["drivers"] = db_ops.get_session(inputs)
        response["constructors"] = db_ops.get_session_constructors(
            inputs, response["drivers"]
        )
    except ValueError:
        response = False
        print("No data found:", response)
    rr_to_DBmain().main(item=inputs)
    return {"status": "success", "entity": response}


@router.post("/submit/")
def send_info_to_DBs(item: Item):
    inputs = {}
    for entity in list(item):
        inputs[entity[0]] = entity[1]
    # print(inputs)
    response = db_ops.get_session(inputs)
    return {"status": "success", "entity": response}
    # 3) Also add some timed effect that slowly changes positions of driver positions if the inputs change.  4) Update readme how to merge to prod branch and push to prod as well."}
