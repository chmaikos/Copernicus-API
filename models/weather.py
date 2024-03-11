from pydantic import BaseModel
from typing import List
from datetime import datetime


class WeatherDataItem(BaseModel):
    humidity: float
    latitude: float
    longitude: float
    pressure: float
    sea_temp: float
    temperature: float
    time: datetime
    total_cloud_cover: float
    total_rain_water: float
    total_snow_water: float


class WeatherDataResponse(BaseModel):
    weatherData: List[WeatherDataItem]