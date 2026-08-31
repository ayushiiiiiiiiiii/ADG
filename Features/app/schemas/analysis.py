from pydantic import BaseModel
from typing import Dict, Any

class AnalyzeRequest(BaseModel):
    code: str

class AnalyzeResponse(BaseModel):
    language: str
    features: Dict[str, Any]
