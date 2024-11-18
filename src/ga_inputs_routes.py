from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel
from weekend_parse import get_gp_info,gp_parse,sessions_parse
import yaml

router = APIRouter()
class Item(BaseModel):
    year: Optional[int] = None
    raceLoc: Optional[str] = None
    weekly_budget: Optional[float] = None
    max_gens: Optional[int] = None
    pop_size: Optional[int] = None
    crossover: Optional[float] = None
    mutation: Optional[float] = None
    elitism: Optional[int] = None
    tournament_size: Optional[int] = None
    max_drivers: Optional[int] = None
    max_constructors: Optional[int] = None
    
@router.get('/gp_locs/')
def send_gp_dropdown():
    gp_locs = gp_parse(get_gp_info())
    return {'entity':gp_locs}

@router.post('/inputs_submit/')
def inputs_submit(item: Item):
    inputs = {}
    to_yaml_file = {}
    for entity in list(item):
        inputs[entity[0]] = entity[1]
    response = inputs
    tournament_size_prop = inputs['tournament_size']/inputs['pop_size']
    to_yaml_file["weekly_budget"] = inputs["weekly_budget"]
    to_yaml_file["max_gens"] = inputs["max_gens"]
    to_yaml_file["pop_size"] = inputs["pop_size"]
    to_yaml_file["tournament_size_prop"] = tournament_size_prop
    to_yaml_file["crossover"] = inputs["crossover"]
    to_yaml_file["mutation"] = inputs["mutation"]
    to_yaml_file["elitism"] = inputs["elitism"]
    to_yaml_file["max_drivers"] = inputs["max_drivers"]
    to_yaml_file["max_constructors"] = inputs["max_constructors"]
    with open('./input_files/inputs.yaml', 'w+') as outfile:
        yaml.dump(to_yaml_file, outfile, default_flow_style=False)
    return {"status":"success","entity":response}