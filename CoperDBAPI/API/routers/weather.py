from database import db
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/weather")
async def get_weather_data():
    try:
        collection = db["weatherData"]
        results = await collection.find().to_list(None)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
