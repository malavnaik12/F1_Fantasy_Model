from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel
from weekend_parse import get_gp_info,gp_parse,sessions_parse

router = APIRouter()
class Item(BaseModel):
    year: Optional[int] = None
    raceLoc: Optional[str] = None
    session: Optional[str] = None
    drivers: Optional[list] = None
    driver_prices: Optional[list] = None
    constructors: Optional[list] = None
    constructor_prices: Optional[list] = None
    
@router.get('/gp_locs/')
async def send_gp_dropdown():
    gp_locs = gp_parse(get_gp_info())
    return {'entity':gp_locs}

@router.post('/sessions/')
async def send_session_types(item: Item):
    return {'entity':sessions_parse(item.raceLoc)}