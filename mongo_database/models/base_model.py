from pydantic import BaseModel
from typing import List

# Define a baseline model for Constructors and Drivers
class Constructors(BaseModel):
    race_weekend: str
    name: str
    fp: List[float]
    quali_hist: List[float]
    race_hist: List[float]
    price: List[float]
    version: int