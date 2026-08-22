from pydantic import BaseModel
from typing import Dict, Any

class AnalyzeRequest(BaseModel):
    language: str
    code: str

class AnalyzeResponse(BaseModel):
    language: str
    time_complexity: str
    confidence: float
    reason: str
    features: Dict[str, Any]
