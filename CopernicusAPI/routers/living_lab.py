from datetime import datetime

from bson import json_util
from database import db
from fastapi import APIRouter, HTTPException, Query

router = APIRouter()


@router.get("/living_lab")
async def get_living_lab_data(date_min: str = Query(...), date_max: str = Query(...)):
    try:
        date_min_format = datetime.strptime(date_min, "%Y-%m-%dT%H:%M:%S")
        date_max_format = datetime.strptime(date_max, "%Y-%m-%dT%H:%M:%S")

        query = {
            "formattedDate": {
                "$gte": date_min_format.strftime("%d/%m/%Y %H:%M:%S"),
                "$lte": date_max_format.strftime("%d/%m/%Y %H:%M:%S"),
            }
        }

        results = await db["living_lab"].find(query).to_list(None)
        return json_util.dumps(results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
