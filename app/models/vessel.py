from typing import List, Optional

from pydantic import BaseModel


class Step(BaseModel):
    no: int
    description: str


class COP(BaseModel):
    id: Optional[str] = None
    message_type: Optional[str] = None
    threat_name: Optional[str] = None
    threat_description: Optional[str] = None
    steps: Optional[List[Step]] = None


class AlertStep(BaseModel):
    no: int
    description: str
    status: Optional[str] = None


class Alert(BaseModel):
    msg_id: Optional[str] = None
    message_type: Optional[str] = None
    threat_name: Optional[str] = None
    threat_description: Optional[str] = None
    steps: Optional[List[AlertStep]] = None
    rec_steps: Optional[List[AlertStep]] = None
