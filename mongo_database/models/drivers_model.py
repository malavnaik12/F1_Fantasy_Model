from pydantic import BaseModel
from typing import List

# Define a baseline model for Constructors and Drivers
class Drivers(BaseModel):
    race_weekend: str
    team_name: str
    name: str
    number: int
    fp: List[float]
    quali_hist: List[float]
    race_hist: List[float]
    price: List[float]
    version: int