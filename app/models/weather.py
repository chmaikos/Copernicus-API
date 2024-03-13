from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Location(BaseModel):
    type: str
    coordinates: List[float]  # [longitude, latitude]


class WeatherDataItem(BaseModel):
    time: datetime = Field(..., example="2024-03-07T00:00:00.000Z")
    temperature: float = Field(..., example=277.60692928362465)
    humidity: float = Field(..., example=87.44558066234954)
    pressure: float = Field(..., example=99700.4405242397)
    sea_temp: Optional[float] = Field(None, example="NaN")
    total_cloud_cover: float = Field(..., example=52.829351806885114)
    total_rain_water: float = Field(..., example=0)
    total_snow_water: float = Field(..., example=0.000011042425997864758)
    location: Location

    @property
    def latitude(self) -> float:
        return self.location.coordinates[1]

    @property
    def longitude(self) -> float:
        return self.location.coordinates[0]

    class Config:
        allow_population_by_field_name = True


class WeatherDataResponse(BaseModel):
    weatherData: List[WeatherDataItem]
