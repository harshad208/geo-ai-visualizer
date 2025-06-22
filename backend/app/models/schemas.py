from pydantic import BaseModel
from typing import List, Dict, Any

class QueryRequest(BaseModel):
    query: str

class GeoPoint(BaseModel):
    type: str = "Feature"
    geometry: Dict[str, Any]
    properties: Dict[str, Any]

class QueryResponse(BaseModel):
    action_triggered: str
    data: List[GeoPoint]