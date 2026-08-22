from fastapi import APIRouter, HTTPException
from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse
from app.analyzers.python_analyzer import PythonAnalyzer
from app.analyzers.java_analyzer import JavaAnalyzer
from app.ml.predictor import ComplexityPredictor
from app.explanation.explainer import ComplexityExplainer

router = APIRouter()

# Instantiate globally so they are reused
predictor = ComplexityPredictor()
explainer = ComplexityExplainer()

python_analyzer = PythonAnalyzer()
java_analyzer = JavaAnalyzer()

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_code(request: AnalyzeRequest):
    code = request.code.strip()
    language = request.language.strip().lower()
    
    if not code:
        raise HTTPException(status_code=400, detail="Code cannot be empty.")
        
    try:
        # 1. Parse and extract features
        if language == "python":
            features = python_analyzer.analyze(code)
        elif language == "java":
            features = java_analyzer.analyze(code)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported language: {language}")
            
        # 2. Predict time complexity
        prediction, confidence = predictor.predict(features)
        
        # 3. Generate explanation
        reason = explainer.explain(features, prediction)
        
        # 4. Construct response
        return AnalyzeResponse(
            language=language,
            time_complexity=prediction,
            confidence=round(confidence, 2),
            reason=reason,
            features=features.to_dict()
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/health")
def health_check():
    return {"status": "ok"}
