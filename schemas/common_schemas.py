from pydantic import BaseModel
from typing import List, Optional, Dict



class ByUserPathSchema(BaseModel):
    user_id: str


class ByPeriodQueryParamSchema(BaseModel):
    initialDate: str
    endDate: str


class MessageSchema(BaseModel):
    message: str


class ErrorsInfo(BaseModel):
    locations: List[Dict[str, int]]
    message: str
    path: Optional[List[str]]


class ErrorSchema(BaseModel):
    data: None
    errors: List[ErrorsInfo]
