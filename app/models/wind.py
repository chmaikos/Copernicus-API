from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class Location(BaseModel):
    type: str
    coordinates: List[float]  # [longitude, latitude]


class WindDataItem(BaseModel):
    time: datetime = Field(..., example="2024-03-07T00:00:00.000Z")
    u10: float = Field(..., example=-0.406362167404559)
    v10: float = Field(..., example=-0.9987803144060436)
    speed: float = Field(..., example=1.0782821187160465)
    direction: float = Field(..., example=22.13936299866566)
    location: Location

    @property
    def latitude(self) -> float:
        return self.location.coordinates[1]

    @property
    def longitude(self) -> float:
        return self.location.coordinates[0]

    class Config:
        allow_population_by_field_name = True


class WindDataResponse(BaseModel):
    windData: List[WindDataItem]
