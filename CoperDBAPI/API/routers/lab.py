import json
import re

from database import db
from fastapi import APIRouter, HTTPException, Request

router = APIRouter()


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
