from datetime import datetime

from database import db
from fastapi import APIRouter, HTTPException
from models.weather import WeatherDataResponse, WeatherDataItem

router = APIRouter()

@router.get("/weather", response_model=WeatherDataResponse)
async def get_weather_data():
    try:
        collection = db["weatherData"]
        results = await collection.find().to_list(None)

        # Process results to match the desired output format
        processed_results = []
        for item in results:
            if isinstance(item["time"], str):
                item["time"] = datetime.strptime(item["time"], "%d/%m/%Y %H:%M:%S")
            processed_results.append(WeatherDataItem(**item))
            del item["_id"]
            processed_results.append(item)

        return {"weatherData": processed_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
