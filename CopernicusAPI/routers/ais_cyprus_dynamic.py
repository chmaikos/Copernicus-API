from datetime import datetime, timedelta

from bson import json_util
from database import db
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/ais_cyprus_dynamic")
async def get_ais_cyprus_dynamic(date_min: str, date_max: str):
    try:
        date_min_format = datetime.strptime(date_min, "%Y-%m-%dT%H:%M:%S")
        date_max_format = datetime.strptime(date_max, "%Y-%m-%dT%H:%M:%S")

        if date_max_format - date_min_format > timedelta(hours=2):
            date_min_format = date_max_format - timedelta(hours=2)

        collection = db["ais_cyprus_dynamic"]
        query = {"timestamp": {"$gte": date_min_format, "$lte": date_max_format}}
        results = await collection.find(query).to_list(None)
        return json_util.dumps(results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
