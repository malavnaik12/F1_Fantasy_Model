from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel
from weekend_parse import get_gp_info, gp_parse, sessions_parse
import yaml
from main_ga import MainGA

router = APIRouter()


class Item(BaseModel):
    year: Optional[int] = None
    raceLoc: Optional[str] = None


@router.get("/gp_locs/")
def send_gp_dropdown():
    gp_locs = gp_parse(get_gp_info())
    return {"entity": gp_locs}


@router.post("/generate_team/")
def generate_team(item: Item):
    inputs = {}
    for entity in list(item):
        inputs[entity[0]] = entity[1]
    response = MainGA().genetic_algorithm(item=inputs)
    return {"entity": response}
