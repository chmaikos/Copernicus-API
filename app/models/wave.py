from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class Location(BaseModel):
    type: str
    coordinates: List[float]  # (longitude, latitude)


class WaveDataItem(BaseModel):
    time: datetime
    vhm0: float = Field(..., alias="wave_height")
    vmdr: float = Field(..., alias="wave_direction")
    vtm10: float = Field(..., alias="wave_period")
    location: Location

    @property
    def latitude(self) -> float:
        return self.location.coordinates[1]

    @property
    def longitude(self) -> float:
        return self.location.coordinates[0]

    class Config:
        allow_population_by_field_name = True


class WaveDataResponse(BaseModel):
    waveData: List[WaveDataItem]
