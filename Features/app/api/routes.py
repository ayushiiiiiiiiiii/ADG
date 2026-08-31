from fastapi import APIRouter, HTTPException
from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse
from app.analyzers.python_analyzer import PythonAnalyzer
from app.analyzers.java_analyzer import JavaAnalyzer

router = APIRouter()

python_analyzer = PythonAnalyzer()
java_analyzer = JavaAnalyzer()

@router.post("/analyze/python", response_model=AnalyzeResponse)
def analyze_python(request: AnalyzeRequest):
    code = request.code.strip()
    if not code:
        raise HTTPException(status_code=400, detail="Code cannot be empty.")
        
    try:
        features = python_analyzer.analyze(code)
        return AnalyzeResponse(
            language="python",
            features=features.to_dict()
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/analyze/java", response_model=AnalyzeResponse)
def analyze_java(request: AnalyzeRequest):
    code = request.code.strip()
    if not code:
        raise HTTPException(status_code=400, detail="Code cannot be empty.")
        
    try:
        features = java_analyzer.analyze(code)
        return AnalyzeResponse(
            language="java",
            features=features.to_dict()
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/health")
def health_check():
    return {"status": "ok"}
