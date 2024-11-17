from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel
from weekend_parse import get_gp_info,gp_parse,sessions_parse

router = APIRouter()
class Item(BaseModel):
    year: Optional[int] = None
    raceLoc: Optional[str] = None
    budget: Optional[float] = None
    max_gens: Optional[int] = None
    pop_set: Optional[int] = None
    crossover_rate: Optional[float] = None
    mutation_rate: Optional[float] = None
    elite_counts: Optional[int] = None
    tournament_size: Optional[int] = None
    max_drivers_num: Optional[int] = None
    max_constructors_num: Optional[int] = None
    
@router.get('/gp_locs/')
def send_gp_dropdown():
    gp_locs = gp_parse(get_gp_info())
    return {'entity':gp_locs}

@router.post('/inputs_submit/')
def inputs_submit(item: Item):
    inputs = {}
    for entity in list(item):
        inputs[entity[0]] = entity[1]
    response = inputs
    print(inputs)
    return {"status":"success","entity":response}