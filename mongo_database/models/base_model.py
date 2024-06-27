
from pydantic import BaseModel
from typing import List
# Define a Pydantic model
class Item(BaseModel):
    name: str
    fp: List[float]
    quali_hist: List[float]
    race_hist: List[float]
    price: List[float]