import math
from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, Query

from pydantic import BaseModel

from models.wave import WaveDataItem
from models.wind import WindDataItem
from models.weather import WeatherDataItem
from database import db

class CombinedDataResponse(BaseModel):
    weatherData: List[WeatherDataItem] = []
    waveData: List[WaveDataItem] = []
    windData: List[WindDataItem] = []

router = APIRouter()

def create_square(lat1, lon1, distance_km):
    R = 6371  # Radius of the Earth in kilometers
    lat1, lon1 = map(math.radians, [lat1, lon1])  # Convert lat/lon to radians

    # Define bearings
    directions = {"north": 0, "south": 180, "east": 90, "west": 270}
    new_coords = {}

    for key, bearing in directions.items():
        bearing = math.radians(bearing)
        new_lat = math.asin(
            math.sin(lat1) * math.cos(distance_km / R)
            + math.cos(lat1) * math.sin(distance_km / R) * math.cos(bearing)
        )
        new_lon = lon1 + math.atan2(
            math.sin(bearing) * math.sin(distance_km / R) * math.cos(lat1),
            math.cos(distance_km / R) - math.sin(lat1) * math.sin(new_lat),
        )
        new_coords[key] = (math.degrees(new_lat), math.degrees(new_lon))

    return new_coords

@router.get("/data", response_model=CombinedDataResponse)
async def get_data(
    latitude: float = Query(...),
    longitude: float = Query(...),
    radius: float = Query(...),
    dateMin: str = Query(...),
    dateMax: str = Query(...),
):
    try:
        coords = create_square(latitude, longitude, radius)
        date_min_format = datetime.strptime(dateMin, "%Y-%m-%dT%H:%M:%S.%fZ")
        date_max_format = datetime.strptime(dateMax, "%Y-%m-%dT%H:%M:%S.%fZ")

        polygon_coordinates = [
            [coords["west"][1], coords["south"][0]],
            [coords["east"][1], coords["south"][0]],
            [coords["east"][1], coords["north"][0]],
            [coords["west"][1], coords["north"][0]],
            [coords["west"][1], coords["south"][0]],
        ]

        query = {
            "time": {"$gte": date_min_format, "$lte": date_max_format},
            "coordinates": {"$geoWithin": {"$geometry": {"type": "Polygon", "coordinates": [polygon_coordinates]}}}
        }

        combined_response = CombinedDataResponse(waveData=[], windData=[], weatherData=[])
        collections = {
            "waveData": (WaveDataItem, "waveData"),
            "windData": (WindDataItem, "windData"),
            "weatherData": (WeatherDataItem, "weatherData"),
        }

        for collection_name, (model, attr) in collections.items():
            raw_data = await db[collection_name].find(query).to_list(None)
            processed_data = []
            for item in raw_data:
                if "time" in item and isinstance(item["time"], str):
                    item["time"] = datetime.strptime(item["time"], "%d/%m/%Y %H:%M:%S")
                if "_id" in item:
                    del item["_id"]
                processed_data.append(model(**item))  
            setattr(combined_response, attr, processed_data)

        return combined_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
