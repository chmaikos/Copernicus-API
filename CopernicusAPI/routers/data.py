import math
from datetime import datetime

from bson import json_util
from database import db
from fastapi import APIRouter, HTTPException, Query

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


@router.get("/data")
async def get_data(
    latitude: float = Query(...),
    longitude: float = Query(...),
    radius: float = Query(...),
    date_min: str = Query(...),
    date_max: str = Query(...),
):
    try:
        coords = create_square(latitude, longitude, radius)
        date_min_format = datetime.strptime(date_min, "%Y-%m-%dT%H:%M:%S")
        date_max_format = datetime.strptime(date_max, "%Y-%m-%dT%H:%M:%S")

        query = {
            "coordinates": {
                "$geoWithin": {
                    "$geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [coords["west"][1], coords["south"][0]],  # Bottom-left
                                [coords["east"][1], coords["south"][0]],  # Bottom-right
                                [coords["east"][1], coords["north"][0]],  # Top-right
                                [coords["west"][1], coords["north"][0]],  # Top-left
                                [
                                    coords["west"][1],
                                    coords["south"][0],
                                ],  # Closing the loop
                            ]
                        ],
                    }
                }
            },
            "date": {"$gte": date_min_format, "$lte": date_max_format},
        }

        results = []
        for collection_name in [
            "waveData",
            "windData",
            "weatherData",
        ]:  # Example collection names
            collection = db[collection_name]
            data = await collection.find(query).to_list(None)
            results.append({collection_name: data})

        return json_util.dumps(results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
