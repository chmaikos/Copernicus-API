from fastapi import APIRouter, HTTPException, Query
from typing import List
from database import db_vessel
from models.vessel import COP, Alert

router = APIRouter()

@router.get("/threats/", response_model=List[COP])
async def get_cops():
    cursor = db_vessel["COPs"].find({}, {"id": 1, "threat_name": 1})
    cops = await cursor.to_list(length=None)
    return cops

@router.get("/threat-cops/", response_model=COP)
async def get_cops_for_threat(id: str = Query(...)):
    cop = await db_vessel["COPs"].find_one({"id": id})
    if not cop:
        raise HTTPException(status_code=404, detail="COP not found")
    return cop

@router.put("/update-cops/", response_model=COP)
async def update_steps(id: str, cop_update: COP):
    updated_cop = await db_vessel["COPs"].find_one_and_update({"id": id}, {"$set": cop_update.dict(exclude_unset=True)}, return_document=True)
    if updated_cop is None:
        raise HTTPException(status_code=404, detail="COP not found")
    return updated_cop

@router.get("/rops/", response_model=Alert)
async def get_rops(msg_id: str = Query(...)):
    alert = await db_vessel["alerts"].find_one({"msg_id": msg_id})
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    steps_set = {step["description"] for step in alert["steps"]}
    rec_steps_set = {step["description"] for step in alert["rec_steps"]}
    diff = list(steps_set.difference(rec_steps_set))
    alert["other_steps"] = diff
    return alert

@router.put("/update-status-and-rops/", response_model=Alert)
async def update_rops(msg_id: str, alert_update: Alert):
    updated_alert = await db_vessel["alerts"].find_one_and_update({"msg_id": msg_id}, {"$set": alert_update.dict(exclude_unset=True)}, return_document=True)
    if updated_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return updated_alert