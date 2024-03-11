from datetime import datetime
import json
import re

from bson import json_util
from database import db
from fastapi import APIRouter, HTTPException, Request, Query

router = APIRouter()


@router.get("/lab")
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

@router.post("/lab")
async def add_data(request: Request):
    try:
        json_data = await request.json()
        data_str = json.dumps(json_data)
        pattern = r'"id":(\w+)'
        data_with_quotes = re.sub(pattern, lambda x: f'"id":"{x.group(1)}"', data_str)
        data_list = json.loads(data_with_quotes)

        await db["living_lab"].insert_many(data_list)
        return {"message": "Data added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))