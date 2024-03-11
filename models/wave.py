from pydantic import BaseModel
from typing import List
from datetime import datetime

class WaveDataItem(BaseModel):
    time: datetime
    latitude: float
    longitude: float
    wave_height: float
    wave_period: float
    wave_direction: int

class WaveDataResponse(BaseModel):
    waveData: List[WaveDataItem]