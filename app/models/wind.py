from pydantic import BaseModel
from typing import List
from datetime import datetime

class WindDataItem(BaseModel):
    time: datetime
    latitude: float
    longitude: float
    wind_speed: float
    wind_direction: int

class WindDataResponse(BaseModel):
    windData: List[WindDataItem]