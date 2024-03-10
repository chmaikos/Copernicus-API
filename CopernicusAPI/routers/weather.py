from bson import json_util
from database import db
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/weather")
async def get_weather_data():
    try:
        collection = db["weatherData"]
        results = await collection.find().to_list(None)
        return json_util.dumps(results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
